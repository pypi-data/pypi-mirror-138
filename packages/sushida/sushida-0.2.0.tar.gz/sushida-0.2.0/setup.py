# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sushida']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==8.3.1',
 'PyYAML',
 'filesystem-python==0.2.0',
 'optext-python==0.1.1',
 'pyautogui',
 'pytesseract==0.3.7',
 'python-xlib',
 'selenium',
 'webdriver-manager']

extras_require = \
{'docs': ['furo',
          'myst-parser',
          'pdoc3',
          'pydata-sphinx-theme',
          'python-docs-theme',
          'sphinx',
          'sphinx-book-theme',
          'sphinx-theme-pd',
          'sphinx_rtd_theme<=2.0.0',
          'sphinxcontrib-mermaid']}

entry_points = \
{'console_scripts': ['sushida = sushida.cli:main']}

setup_kwargs = {
    'name': 'sushida',
    'version': '0.2.0',
    'description': 'Sushida API for Python',
    'long_description': '# sushida-py\nThe RPA tool for Sushida with Python\n\n\n# Environment\n- ubuntu:20.04\n- [docker](https://www.docker.com/)\n- [docker-compose](https://docs.docker.com/compose/install/)\n\n\n# Usage\n## start\n```sh\n$ xhost + \\\n  && cd ./env/docker/ \\\n  && docker-compose up\n```\n\n## stop forcely\n```sh\n$ docker-compose down\n```\n\n\n## Sample result\nThe screenshot of the result is saved as `data/result.png`\nafter the program done successfly.\n![score](./docs/static/score.png)\n![rank](./docs/static/rank.png)\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/sushida-python#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
