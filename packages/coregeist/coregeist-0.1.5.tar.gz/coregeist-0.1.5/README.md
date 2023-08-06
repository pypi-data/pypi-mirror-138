# bitgeist

bitgeist is a Python library to convert deep neural network models into c source code.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bitgeist.

```bash
pip install coregeist
```

## Usage

```python
import coregeist as cg

# transform a pytorch model to c code
print(cg.transform(model))

```

Example:

````python
    ...

import coregeist as cg

...


class MnistModel(nn.Module):

    def __init__(self):
        super(MnistModel, self).__init__()

        inputs = 28 * 28
        hidden = 120
        output = 10

        self.l1 = cg.Linear(inputs, hidden, downsample=downsample)
        self.action = nn.PReLU(hidden)
        self.l2 = cg.Linear(hidden, output, downsample=downsample)

    def forward(self, x):
        out = self.l1(x)
        out = self.action(out)
        out = self.l2(out)
        return out


model = MnistModel().to(device)

# train the model 

...

print(cg.transform(model))  # print or write to file ...
...
````

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
