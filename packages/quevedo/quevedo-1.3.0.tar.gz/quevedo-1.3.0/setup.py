# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quevedo',
 'quevedo.annotation',
 'quevedo.darknet',
 'quevedo.network',
 'quevedo.web']

package_data = \
{'': ['*'], 'quevedo.web': ['static/*', 'static/i18n/*', 'static/lib/*']}

install_requires = \
['click>=8,<9', 'pillow>=8,<9', 'toml>=0.10.2,<0.11.0']

extras_require = \
{'force_layout': ['forcelayout>=1.0.6,<2.0.0'], 'web': ['flask>=1.1.2,<2.0.0']}

entry_points = \
{'console_scripts': ['quevedo = quevedo.cli:cli']}

setup_kwargs = {
    'name': 'quevedo',
    'version': '1.3.0',
    'description': 'Tool for managing datasets of images with compositional semantics',
    'long_description': '![Quevedo Logo](quevedo/logo.png)\n\n# Quevedo\n\nQuevedo is a python tool for creating, annotating and managing datasets of\ngraphical languages, with a focus on the training and evaluation of machine\nlearning algorithms for their recognition.\n\nQuevedo is part of the [VisSE project](https://www.ucm.es/visse). The code can\nbe found at [GitHub](https://github.com/agarsev/quevedo), and [detailed\ndocumentation here](https://agarsev.github.io/quevedo).\n\n## Features\n\n- Dataset management, including hierarchical dataset organization, subset\n    partitioning, and semantically guided data augmentation.\n- Structural annotation of source images using a web interface, with support for\n    different users and the live visualization of data processing scripts.\n- Deep learning network management, training, configuration and evaluation,\n    using [darknet].\n\n## Installation\n\nQuevedo requires `python >= 3.7`, and can be installed from\n[PyPI](https://pypi.org/project/quevedo/):\n\n```shell\n$ pip install quevedo\n```\n\nOr, if you want any extras, like the web interface:\n\n```shell\n$ pip install quevedo[web]\n```\n\nOr directly from the wheel in the [release\nfile](https://github.com/agarsev/quevedo/releases):\n\n```shell\n$ pip install quevedo-{version}-py3-none-any.whl[web]\n```\n\nYou can test that quevedo is working\n\nTo use the neural network module, you will also need [to install\ndarknet](https://agarsev.github.io/quevedo/latest/nets/#installation).\n\n## Usage\n\nTo create a dataset:\n\n```shell\n$ quevedo -D path/to/new/dataset create\n```\n\nThen you can **cd** into the dataset directory so that the `-D` option is not\nneeded.\n\nYou can also download an example dataset from this repository (`examples/toy_arithmetic`).\n\nTo see information about a dataset:\n\n```shell\n$ quevedo info\n```\n\nTo launch the web interface (you must have installed the "web" extra):\n\n```shell\n$ quevedo web\n```\n\nFor more information, and the list of commands, run `quevedo --help` or `quevedo\n<command> --help` or see [here](https://agarsev.github.io/quevedo/latest/cli/).\n\n## Development\n\nTo develop on quevedo, we use [poetry] as our environment, dependency and build\nmanagement tool. In the quevedo code directory, run:\n\n```shell\n$ poetry install\n```\n\nThen you can run quevedo with\n\n```shell\n$ poetry run quevedo\n```\n\n## Dependencies\n\nQuevedo makes use of the following open source projects:\n\n- [python 3]\n- [poetry]\n- [darknet]\n- [click]\n- [flask]\n- [preactjs]\n\nAdditionally, we use the [toml] and [forcelayout] libraries, and build our\ndocumentation with [mkdocs].\n\n## About\n\nQuevedo is licensed under the [Open Software License version\n3.0](https://opensource.org/licenses/OSL-3.0).\n\nThe web interface includes a copy of [preactjs] for ease of offline use, distributed\nunder the [MIT License](https://github.com/preactjs/preact/blob/master/LICENSE).\n\nQuevedo is part of the project ["Visualizando la SignoEscritura" (Proyecto VisSE,\nFacultad de Informática, Universidad Complutense de\nMadrid)](https://www.ucm.es/visse) as part of the\nprogram for funding of research projects on Accesible Technologies financed by\nINDRA and Fundación Universia. An expert system developed using Quevedo is\ndescribed [in this article](https://eprints.ucm.es/id/eprint/69235/).\n\n### VisSE team\n\n- [Antonio F. G. Sevilla](https://github.com/agarsev) <afgs@ucm.es>\n- [Alberto Díaz Esteban](https://www.ucm.es/directorio?id=20069)\n- [Jose María Lahoz-Bengoechea](https://ucm.es/lengespyteoliter/cv-lahoz-bengoechea-jose-maria)\n\n[darknet]: https://pjreddie.com/darknet/install/\n[poetry]: https://python-poetry.org/\n[python 3]: https://www.python.org/\n[click]: https://click.palletsprojects.com/\n[flask]: https://flask.palletsprojects.com/en/2.0.x/\n[preactjs]: https://preactjs.com/\n[toml]: https://pypi.org/project/toml/\n[forcelayout]: https://pypi.org/project/forcelayout/\n[mkdocs]: https://www.mkdocs.org/\n',
    'author': 'Antonio F. G. Sevilla',
    'author_email': 'afgs@ucm.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agarsev/quevedo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
