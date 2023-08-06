# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csw93']

package_data = \
{'': ['*'], 'csw93': ['data/*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'pandas>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'csw93',
    'version': '0.1.0',
    'description': 'Regular Fractional Factorial two-level designs from the paper of Chen, Sun and Wu (1993)',
    'long_description': '# csw93\n\nCSW93 is a Python package that generates all regular fractional factorial two-level designs from the 1993 paper of Chen, Sun and Wu: ["A catalogue of two-level and three-level fractional factorial designs with small runs"](1).\n\n[1]: <https://www.jstor.org/stable/1403599>\n\n## Instalation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install csw93.\n\n```bash\npip install csw93\n```\n\n## Usage\n\nThe pakage provides three function to get\n\n- The design matrix,\n- The word length pattern,\n- The number of clear two-factor interactions,\n\nusing only the number of runs and the index of the design.\nThis index corresponds to the first column in all tables of all tables from the paper.\n\n```python\nimport csw93\n\n# Design matrix of the 16-run design with index 8-4.1\ncsw93.get_design(16, "8-4.1")\n\n# Word length pattern of the 32-run design with index 15-10.2\ncsw93.get_wlp(16, "8-4.1")\n\n# Number of clear two-factor interactions for the 64-run design 11-5.10\ncsw93.get_cfi(64, "11-5.10")\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Alexandre Bohyn',
    'author_email': 'alexandre.bohyn@kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ABohynDOE/csw93',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
