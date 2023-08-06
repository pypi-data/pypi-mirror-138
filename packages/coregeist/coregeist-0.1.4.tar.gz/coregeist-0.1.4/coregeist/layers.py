import torch
import torch.nn as nn
import torch.nn.functional as F

__all__ = ["LearnableBiasDense", "BinaryActivation"]


def get_weight(module):
    std, mean = torch.std_mean(
        module.weight, dim=[1, 2, 3], keepdim=True, unbiased=False
    )
    weight = (module.weight - mean) / (std + module.eps)
    return weight


# Calculate symmetric padding for a convolution
def get_padding(kernel_size: int, stride: int = 1, dilation: int = 1, **_) -> int:
    padding = ((stride - 1) + dilation * (kernel_size - 1)) // 2
    return padding


class LearnableBiasDense(nn.Module):
    """The bias of the activation"""

    def __init__(self, out_chn):
        super(LearnableBiasDense, self).__init__()
        self.bias = nn.Parameter(torch.zeros(out_chn), requires_grad=True)

    def forward(self, x):
        out = x + self.bias.expand_as(x)
        return out

    def bias_values(self, resolution: int = 1):
        return [int(x) for x in torch.mul(self.bias, resolution).detach().tolist()]

    def bias_params(self):
        return self.bias.detach().tolist()


class BinaryActivation(nn.Module):
    def __init__(self):
        super(BinaryActivation, self).__init__()
        self.out_forward = None

    def forward(self, x):
        self.out_forward = torch.sign(x)
        # just return the sign [-1,1] if the module is not in training mode
        if not self.training:
            return self.out_forward
        # out_e1 = (x^2 + 2*x)
        # out_e2 = (-x^2 + 2*x)
        #        out_e_total = 0
        mask1 = x < -1
        mask2 = x < 0
        mask3 = x < 1
        # if x < -1: -1 else: x*x+2*x
        out1 = (-1) * mask1.type(torch.float32) + (x * x + 2 * x) * (
                1 - mask1.type(torch.float32)
        )
        # if x < 0: 1 else: -x*x+2*x
        out2 = out1 * mask2.type(torch.float32) + (-x * x + 2 * x) * (
                1 - mask2.type(torch.float32)
        )
        # if x < -1: -1
        # if x >= -1 and x < 0: x * x + 2 * x
        # if x >=  0 and x < 1: -x * x + 2 * x
        # if x >= 1: 1
        out3 = out2 * mask3.type(torch.float32) + 1 * (1 - mask3.type(torch.float32))
        out = self.out_forward.detach() - out3.detach() + out3

        return out


class HardBinary(nn.Module):
    def __init__(self, in_chn, out_chn):
        super(HardBinary, self).__init__()
        self.scaling_factor = None
        self.clipped_weights = None
        self.binary_weights = None
        self.number_of_weights = in_chn * out_chn
        self.shape = (out_chn, in_chn)
        # self.weight = nn.Parameter(torch.rand((self.number_of_weights,1)) * 0.001, requires_grad=True)
        self.weight = nn.Parameter(torch.rand(self.shape) * 0.001, requires_grad=True)

    def forward(self, x):
        """
        the forward process binarized the weights matrix before the matrix multiplication with the activation x
        """
        real_weights = self.weight
        self.binary_weights = torch.sign(real_weights)
        self.scaling_factor = torch.mean(abs(real_weights))
        self.scaling_factor = self.scaling_factor.detach()
        if not self.training:
            return F.linear(x, self.binary_weights) * self.scaling_factor
        # transform the weights to a binary matrix [-scaling_factor, scaling_factor]
        binary_weights_no_grad = self.scaling_factor * self.binary_weights
        # Clamps all elements in the weights matrix into the range [ -1, 1 ].
        cliped_weights = torch.clamp(real_weights, -1.0, 1.0)
        weights = (
                binary_weights_no_grad.detach() - cliped_weights.detach() + cliped_weights
        )
        y = F.linear(x, weights)

        return y


class Linear(nn.Module):
    def __init__(self, input, output, downsample=None):
        super(Linear, self).__init__()
        self.bias = LearnableBiasDense(input)
        self.binary_activation = BinaryActivation()
        self.lin = HardBinary(input, output)
        self.downsample = downsample
        self.num_parameters = input * output

    def forward(self, x):
        x = self.bias(x)
        out = self.binary_activation(x)
        if self.downsample is not None:
            out = self.downsample(out)
        out = self.lin(out)
        return out

    def binary_weights(self):
        return self.lin.binary_weights.detach()

    def conversion_factors(self, bias_factor: int = 1):
        return self.bias.bias_values(bias_factor), self.lin.scaling_factor

    def bias_params(self):
        return self.bias.bias_params()

    def scaling_factor(self):
        return self.lin.scaling_factor
