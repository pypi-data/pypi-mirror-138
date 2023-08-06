# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rootsstyle']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'rootsstyle',
    'version': '0.4.0',
    'description': 'A dataroots inspired theme for matplotlib.',
    'long_description': '[![dataroots](https://dataroots.io/maintained.svg)](https://dataroots.io/)\n[![PyPI version](https://badge.fury.io/py/rootsstyle.svg)](https://badge.fury.io/py/rootsstyle)\n[![Python Versions](https://img.shields.io/badge/python->=3.7.1,%20<3.11-blue.svg)](https://www.python.org/downloads/)\n[![codecov](https://codecov.io/gh/datarootsio/rootsstyle/branch/main/graph/badge.svg?token=4agmmGuhtu)](https://codecov.io/gh/datarootsio/rootsstyle)\n[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)\n\n<div align="center">\n\n# rootsstyle\n</div>\n\nA matplotlib styling package for clean, minimal dataroots themed plots. \nWorks with any visualization tools that builds upon Matplotlib (seaborn, pandas).\n\n<img align="center" src="https://github.com/datarootsio/rootsstyle/blob/main/images/examples.png">\n\n\n\n# Installation\n### using [pip](https://pypi.org/)\n```python\npip install rootsstyle\n```\n### using [poetry](https://python-poetry.org/)\n```python\npoetry add rootsstyle\n```\n\n# Usage\n**Examples**\n\n<a href="https://colab.research.google.com/drive/1kn7YLDR4hqI9GVzeiRH9aQTEeS7HPrw7" target="_blank" rel="noopener noreferrer"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>\n\n<table width="100%">\n<tr>\n<td width="50%"> \n\n```python\nimport rootsstyle\nimport matplotlib.pyplot as plt\n\nplt.style.use(rootsstyle.style)\ny, y2 = [3, 8, 1, 10], [8, 3, 10, 2]\nplt.plot(y, label=\'y\')\nplt.plot(y2, label=\'y2\', linestyle = \'dotted\')\nrootsstyle.ylabel(\'yvalues\')\nplt.xlabel(\'x-label\')\nrootsstyle.legend()\nplt.title(\'Example plot\')\nplt.show()\n```\n\n</td>\n<td width="50%"> \n\n```python\nimport rootsstyle\nimport matplotlib.pyplot as plt\n\nplt.style.use(rootsstyle.style)\nlanguages = [\'C\', \'C++\', \'Java\', \'Python\', \'PHP\']\nstudents = [23,17,35,29,12]\nplt.bar(languages, students)\nplt.xlabel(\'Language\')\nrootsstyle.show_bar_values()\nplt.title(\'Example barplot\')\nplt.show()\n```\n</td>\n</tr>\n<tr>\n<td width="50%"><img src="https://github.com/datarootsio/rootsstyle/blob/main/images/example_lineplot.png"></td>\n<td width="50%"> <img src="https://github.com/datarootsio/rootsstyle/blob/main/images/example_barplot.png"></td>\n</tr>\n</table>\n\n\n**STYLING**\n\n```python\nimport rootsstyle\nimport matplotlib.pyplot as plt\n\n# globally\nplt.style.use(rootsstyle.style)\n\n# within context manager\nwith plt.style.context(rootsstyle.style):\n    # ...\n```\n\n**FUNCTIONS**\n* Place the legend to the right of the plot.<br>For lineplots, place the legend entries right of the corresponding line.\n    ```python \n    rootsstyle.legend(handles=None, labels=None, title=None)\n    ```\n\n* Place the y-label above the y-axis and rotate it, so that it is horizontal.\n    ```python \n    rootsstyle.ylabel(ylabel: str)\n    ```\n* Show barvalues at each bar. <br>Removes the y-axis (optional).<br>Bar values can be shown just \'below\' the top of each bar, or just \'above\' each bar.\n    ```python \n    rootsstyle.show_bar_values(remove_y_axis=True, fontsize=12, position="below", fmt="{:.0f}")\n    ```\n\n \n\n**COLOR PALETTE**\n<table width="100%">\n    <tr>\n        <td width="40%" align="center">The color palettes are added to the global matplotlib color registry. You can thus easily use a palette by simply providing the name in the correct location.</td>\n        <td width="60%" align="center">\n            <img src="https://github.com/datarootsio/rootsstyle/blob/main/images/palette.png" height="350px;">\n        </td>\n    </tr>\n</table>\n\n\n# VERSIONING\n\nA [semantic versioning](https://semver.org/) scheme is used to update the version on the commit messages. This happens automatically on any push to the main branch. Only patches, minor and major changes will generate a tag, release and publishing of the package. We stick to the default [Angular Commit Message Conventions](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines). To use this system, commit messages should adhere to a couple of rules:\n\n1. Commits must follow the following syntax\n\n    ```\n    <type>(<scope>): <subject>\n    <BLANK LINE>\n    <body>\n    <BLANK LINE>\n    <footer>\n    ```\n\n2. Type should be one of the following:\n    * feat: A new feature\n    * fix: A bug fix\n    * docs: Documentation only changes\n    * style: Changes that do not affect the meaning of the code (formatting, missing semi-colons, etc)\n    * refactor: A code change that neither fixes a bug nor adds a feature\n    * perf: A code change that improves performance\n    * test: Adding missing or correcting existing tests\n    * chore: Changes to the build process or auxiliary tools and libraries such as documentation generation\n\n3. Body (optional) is used to motivate the change\n4. Footer (optional) is used to link to any **issues** that the commit closes and for **breaking changes**, in which case the line should start with `BREAKING CHANGE:`.\n\n# CHANGELOG\nThe [CHANGELOG.md](https://github.com/datarootsio/rootsstyle/blob/main/CHANGELOG.md) file is automatically updated upon any new releases.\n\n# License\nThis project is licensed under the terms of the MIT license.',
    'author': 'YannouRavoet',
    'author_email': 'yannou.ravoet@dataroots.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yannouravoet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
