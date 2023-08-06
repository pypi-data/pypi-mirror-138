# seg-text
[![pytest](https://github.com/ffreemt/seg-text/actions/workflows/ubuntu-pytest.yml/badge.svg)](https://github.com/ffreemt/seg-text/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/seg_text.svg)](https://badge.fury.io/py/seg_text)

Segment multilingual text to sentences

### Pre-install PyICU/pycld2/polyglot

#### For Linux and friends
Install `libicu`, for example for Ubuntu:
```bash
apt install libicu-dev
poetry add pyicu==2.8 pycld2 polyglot
```

#### For Windows

`seg-text` depends on `polyglot` which in turn depengs on `pyicu` and `pycld2`. `pyicu` and `pycld2` are difficult if not impossible to install in Windows using pip or poetry.

However, readily available `whl` packages can be downloaded from [https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/) and installed  (for example for python 3.8 amd64) as follows
```bash
pip install PyICU-2.8.1-cp38-cp38-win_amd64.whl pycld2-0.41-cp38-cp38-win_amd64.whl
poetry add git+https://github.com/aboSamoor/polyglot@master
```

Refer to `windows-pytest.yml` and `ubuntu-pytest.yml` in `.github/workflows` for more details.

## Install `seg-text`

```shell
pip install seg-text
# or pip install git+https://github.com/ffreemt/seg-text
# or poetry add git+https://github.com/ffreemt/seg-text
```

## Use `seg-text`
```python
from seg_text import seg_text

prin(seg_text(" text 1\n test 2. Test 3"))
# ["text 1", "test 2.", "Test 3"]

text = """ “元宇宙”，英文為“Metaverse”。該詞出自1992年；的科幻小說《雪崩》。 """
print(seg_text(text))
# ["“元宇宙”，英文為“Metaverse”。", "該詞出自1992年；的科幻小說《雪崩》。"]

print(seg_text(text, extra="[;:]"))
# ["“元宇宙”，英文為“Metaverse”。", "該詞出自1992年；", "的科幻小說《雪崩》。"]

```

Refer to `seg_text.py` for more details.