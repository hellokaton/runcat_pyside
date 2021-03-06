# RunCat by PySide6

A cute running cat animation on your Windows/macOS taskbar.

[![Github issues](https://img.shields.io/github/issues/biezhi/runcat_pyside)](https://github.com/biezhi/runcat_pyside/issues)
[![Github forks](https://img.shields.io/github/forks/biezhi/runcat_pyside)](https://github.com/biezhi/runcat_pyside/network/members)
[![Github stars](https://img.shields.io/github/stars/biezhi/runcat_pyside)](https://github.com/biezhi/runcat_pyside/stargazers)
[![Top language](https://img.shields.io/github/languages/top/biezhi/runcat_pyside)](https://github.com/biezhi/runcat_pyside/)
[![Release](https://img.shields.io/github/v/release/biezhi/runcat_pyside)]()
[![Github license](https://img.shields.io/github/license/biezhi/runcat_pyside)](https://github.com/biezhi/runcat_pyside/)

# Tags

`PyQt` `PySide` `RunCat`

# Demo

![Demo](snapshot/runcat_demo.gif)

You only have to run the RunCat.exe.

# Run

```bash
pip install -r requirements.txt

python run_cat.py
```

# Packaging

```bash
pip install pyinstaller
```

For Windows

```bash
pyinstaller --clean -Fw -i runcat.ico --add-data "resources;./resources" run_cat.py
```

For macOS

```bash
pyinstaller --clean -Fw -i runcat.ico --add-data "resources:./resources" run_cat.py
```

# License

[MIT](LICENSE)

