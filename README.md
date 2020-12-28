# vimbuffer

Edit files and strings in temporary vim (or some other console editor) buffers.

## Installation

#### Requires:

- python3.6+

```
pip3 install vimbuffer
```

## Usage

There's just the one function, `buffer`:

```
vimbuffer.buffer(string: Union[str, NoneType] = None,
                 file: Union[str, NoneType] = None,
                 editor: Union[str, NoneType] = None,
                 fallbacks: Union[List[str], NoneType] = None,
                 name_prefix: Union[str, NoneType] = None) -> str
    Provide one of:
        string: A string to edit in a vimbuffer
        file: A file to edit in a vimbuffer
    If neither is provided, uses an empty string
    editor: editor to override the passed fallbacks/environment variable
    fallbacks: A list of fallbacks for alternate editors (e.g. ['vim', 'vi', 'nano'])
    name_prefix: string prefix for the filename when opening in an editor

    If string is provided, opens the file in an editor, lets the user edit it,
    and returns the string.
    If a file is, it reads the file, lets the user modify the contents, and writes
    back to the file. It also returns the edited file contents.
```

The editor can be overwritten by specifying environment variables, see below for resolution order.

##### Examples

```python
import vimbuffer

# edit a string
prompt_string = "Edit this and put what you want here!"
edited_text = vimbuffer.buffer(string=prompt_string)  # opens vim

# edit a file
vimbuffer.buffer(file=os.path.expanduser("~/.bashrc"), name_prefix="bashrc-")
```

This uses [`tempfile`](https://docs.python.org/3.8/library/tempfile.html) to create temporary files on the system, and launches vim against them. If the environment variable `$EDITOR` is set to a graphical text editor, the process (which in this case would just launch the graphical editor) would end before the user had a chance to edit it. I recommend using terminal text editors instead.

You can specify a list of fallback editors; one you'd like to use instead of `$EDITOR`:

```python
project_description="""
## <my-project>

By <your-name>
"""

edited_desc = vimbuffer.buffer(project_description, fallbacks=["nvim", "vim", "vi", "nano"])
```

Alternatively, if you want to leave your `$EDITOR` as a graphical text editor, you can set the `$VIMBUFFER_EDITOR` environment variable, which trumps all other choices. Specifically, the resolution order is:

- `$VIMBUFFER_EDITOR`
- `editor`
- `fallbacks`(s) passed as keyword arguments in python
- `$EDITOR`
- `vim`
- `vi`

The `name_prefix` exists as a kwarg since temporary files have names that are randomly generated. By passing a prefix, the name becomes something like `/tmp/bashrc-sd43Jds`, so it may give a hint as to which file/what you're editing

## Tests

```
pytest
```
