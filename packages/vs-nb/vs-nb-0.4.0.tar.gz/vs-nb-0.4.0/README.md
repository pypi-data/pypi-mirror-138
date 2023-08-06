# vs_nb

Is a Python package that saves .ipynb as a .py and vice-versa in VS Code.

This is needed because currently the [VS Code jupytext extension](https://github.com/notebookPowerTools/vscode-jupytext) is broken and the [standard jupytext library](https://github.com/mwouts/jupytext) does not work with VS Code notebooks.

A working jupytext extension would be preferred because this package needs to be run manually in a .ipynb cell or an interactive .py cell (# %% syntax) to convert them, rather than happening after every save. You also need to manually type the name of the file into the convert function, rather than it picking it up automatically.

## Installation

To install [**vs_nb**](https://pypi.org/project/vs-nb/0.1.0/) use pip

```bash
pip install vs-nb
```
or GitHub
```bash
pip install git+https://github.com/JamesHuckle/vs-nb.git
```
## Usage

```python
#Inside a .ipynb cell or .py file that is named "test"
from vs_nb import convert     
convert(file_prefix='test', is_py='__file__' in globals())
```

*(Recommendation)* 

Set up **autosave** on VS Code because it does not currently alert when an file open in a tab has been modified on disk (by vs-nb) until you attempt to save it, meaning you could be working on a stale file without knowing it!

To activate autosave put this in your `settings.json` file in VS Code and restart VS Code.
```Python
"files.autoSave": "onFocusChange",
```

Example Bug:
1) Open `.ipynb` and run `convert` function to build a `.py`
2) Make changes to `.ipynb` in a VS Code tab but **do not save**. 
3) Open the .py, make changes, save it, and run convert to build `.ipynb`.
4) Navigating back to the `.ipynb` in the VS Code tab will result in no warning that the `.ipynb` has just been modified, instead it displays the old unsaved changes.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)