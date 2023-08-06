# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coregeist']

package_data = \
{'': ['*'], 'coregeist': ['resources/*']}

install_requires = \
['torch>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'coregeist',
    'version': '0.1.3',
    'description': 'coregeist is a Python library to convert deep neural network models into c source code.',
    'long_description': '# bitgeist\n\nbitgeist is a Python library to convert deep neural network models into c source code.\n\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install bitgeist.\n\n```bash\npip install coregeist\n```\n\n## Usage\n\n```python\nimport coregeist as bg\n\n# transform a pytorch model to c code\nprint(bg.transform(model))\n\n```\n\nExample:\n\n````python\n    ...\n\nimport coregeist as bg\n\n...\n\n\nclass MnistModel(nn.Module):\n\n    def __init__(self):\n        super(MnistModel, self).__init__()\n\n        inputs = 28 * 28\n        hidden = 120\n        output = 10\n\n        self.l1 = pg.Linear(inputs, hidden, downsample=downsample)\n        self.action = nn.PReLU(hidden)\n        self.l2 = pg.Linear(hidden, output, downsample=downsample)\n\n    def forward(self, x):\n        out = self.l1(x)\n        out = self.action(out)\n        out = self.l2(out)\n        return out\n\n\nmodel = MnistModel().to(device)\n\n# train the model \n\n...\n\nprint(bg.transform(model))  # print or write to file ...\n...\n````\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'germar',
    'author_email': 'g.schlegel@geisten.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.12,<4.0.0',
}


setup(**setup_kwargs)
