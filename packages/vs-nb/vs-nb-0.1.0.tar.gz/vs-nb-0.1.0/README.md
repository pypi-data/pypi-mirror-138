# vs_nb

**vs_nb** is a Python library that converts .ipynb into .py and vice-versa in VS Code.

This is needed because currently the [VS Code jupytext extension](https://github.com/notebookPowerTools/vscode-jupytext) is broken and the [standard jupytext library](https://github.com/mwouts/jupytext) does not work with VS Code notebooks.

A working jupytext extension would be preferred, because this package needs to be run manually in a .ipynb cell or an interactive .py cell (# %% syntax) to convert them, rather than happening after every save. You also need to manually type the name of the file into the convert function, rather that it picking it up automatically.

## Installation

To install **vs_nb**.

```bash
pip install vs-nb
```
or
```bash
pip install git+https://github.com/JamesHuckle/vs-nb.git
```
## Usage

```python
#Inside a .ipynb cell or .py file that is named "test"
from vs_nb import convert     
convert(file_name='test')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)