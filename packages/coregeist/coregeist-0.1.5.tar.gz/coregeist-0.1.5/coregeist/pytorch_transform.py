"""C converter for deep neural network pytorch models

This script provides a toolkit to convert pytorch deepl learning models to c.

This file can also be imported as a module and contains the following
functions:

    * transform - transforms a (trained) pytorch module to _C_ source code.


"""
from typing import Callable

import torch.nn as nn

import coregeist.transform as gs
from coregeist.layers import Linear
from coregeist.transform import MetaObjects


def transform(model: nn.Module, input_scaling_factor: int = 255, resolution: int = 100000,
              template: str = "./coregeist/resources/ctemplate.tpl.c"):
    """Initializes the deep neural net layer builder

    Parameters
    ----------
    model : nn.Module
        The root pytorch module to be transformed

    template : str
        _C_ text template

    Returns
    -------
    str
        the transformed c source code.
    """
    meta_info = gs.MetaInfo()
    layers: list[Callable[[gs.MetaInfo], Callable[[str, str, int], MetaObjects]]] = [gs.entry()]
    scaling_factor = input_scaling_factor
    for layer in model.children():
        if type(layer) == Linear:
            values = layer.lin.binary_weights.numpy()
            bias = layer.bias_params()
            scaled_bias = [-int(b * scaling_factor * resolution) for b in bias]
            scaling_factor = 1.0 / layer.scaling_factor()
            m, n = values.shape
            layers += [
                gs.activation_binarization(scaled_bias, resolution),
                gs.dense(m, list(values)),
            ]
        if type(layer) == nn.PReLU:
            scaled_prelu = []
            for p in layer.parameters():
                prelu = p.data
                scaled_prelu = [int(i * 0) for i in prelu]
            layers += [gs.relu(scaled_prelu, 1)]
    layers += [gs.argmax()]

    return gs.model_transform(meta_info.enrich_all(layers), 28 * 28, template)
