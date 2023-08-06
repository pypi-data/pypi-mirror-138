# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seg_text']

package_data = \
{'': ['*']}

install_requires = \
['Morfessor==2.0.6',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'numpy>=1.22.2,<2.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'sentence-splitter>=1.4,<2.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'seg-text',
    'version': '0.1.0',
    'description': 'pack_name descr ',
    'long_description': '# seg-text\n[![pytest](https://github.com/ffreemt/seg-text/actions/workflows/ubuntu-pytest.yml/badge.svg)](https://github.com/ffreemt/seg-text/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/seg_text.svg)](https://badge.fury.io/py/seg_text)\n\nSegment multilingual text to sentences\n\n### Pre-install PyICU/pycld2/polyglot\n\n#### For Linux and friends\nInstall `libicu`, for example for Ubuntu:\n```bash\napt install libicu-dev\npoetry add pyicu==2.8 pycld2 polyglot\n```\n\n#### For Windows\n\n`seg-text` depends on `polyglot` which in turn depengs on `pyicu` and `pycld2`. `pyicu` and `pycld2` are difficult if not impossible to install in Windows using pip or poetry.\n\nHowever, readily available `whl` packages can be downloaded from [https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/) and installed  (for example for python 3.8 amd64) as follows\n```bash\npip install PyICU-2.8.1-cp38-cp38-win_amd64.whl pycld2-0.41-cp38-cp38-win_amd64.whl\npoetry add git+https://github.com/aboSamoor/polyglot@master\n```\n\nRefer to `windows-pytest.yml` and `ubuntu-pytest.yml` in `.github/workflows` for more details.\n\n## Install `seg-text`\n\n```shell\npip install seg-text\n# or pip install git+https://github.com/ffreemt/seg-text\n# or poetry add git+https://github.com/ffreemt/seg-text\n```\n\n## Use `seg-text`\n```python\nfrom seg_text import seg_text\n\nprin(seg_text(" text 1\\n test 2. Test 3"))\n# ["text 1", "test 2.", "Test 3"]\n\ntext = """ “元宇宙”，英文為“Metaverse”。該詞出自1992年；的科幻小說《雪崩》。 """\nprint(seg_text(text))\n# ["“元宇宙”，英文為“Metaverse”。", "該詞出自1992年；的科幻小說《雪崩》。"]\n\nprint(seg_text(text, extra="[;:]"))\n# ["“元宇宙”，英文為“Metaverse”。", "該詞出自1992年；", "的科幻小說《雪崩》。"]\n\n```\n\nRefer to `seg_text.py` for more details.',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/seg-text',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
