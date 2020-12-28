import os
import tempfile
import shutil
import subprocess

from typing import Optional, List


def get_editor(
    editor: Optional[str] = None, editors: Optional[List[str]] = None
) -> str:
    """
    editors: list of kwargs passed by user

    Evaluates editors specified by this order:

    - `$VIMBUFFER_EDITOR`
    - `editor`(s) passed as keyword arguments in python
    - `$EDITOR`
    - `vim`
    - `vi`

    Returns the first editor which has a corresponding binary
    """
    if editor is not None:
        return str(editor)
    _editors: List[str] = editors or []
    editor_list: List[str] = [
        ed.strip()  # type: ignore[union-attr]
        for ed in filter(
            lambda e: e is not None,
            [os.environ.get("VIMBUFFER_EDITOR"), editor]
            + _editors  # type: ignore[operator]
            + [
                os.environ.get("EDITOR"),
                "vim",
                "vi",
            ],
        )
    ]
    for e in editor_list:
        if shutil.which(e):
            return e
    else:
        raise RuntimeError(
            "Could not find any binaries that correspond to the editors: {}".format(
                editor_list
            )
        )


def buffer(
    string: Optional[str] = None,
    file: Optional[str] = None,
    editor: Optional[str] = None,
    fallbacks: Optional[List[str]] = None,
    name_prefix: Optional[str] = None,
) -> str:
    """
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
    """
    EDITOR = get_editor(editor, fallbacks)

    # ensure either string or file was passed
    if string is None:
        if file:
            with open(file) as f:
                string = f.read()
        else:
            string = ""
    else:
        if file:
            raise ValueError(
                "You cannot specify both `string` and `file` as input for a buffer"
            )

    tf = tempfile.NamedTemporaryFile(prefix=name_prefix, delete=False)
    tf.write(string.encode())
    tf.flush()
    subprocess.call([EDITOR, tf.name])
    # cant seek to 0 and try to re-read, that has some issues (e.g. with vim on mac)
    # close and re-open the file
    tf.close()
    with open(tf.name, "r") as mod_tf:
        edited_string = mod_tf.read()
    os.remove(tf.name)

    if file:
        with open(file, "w") as f:
            f.write(edited_string)

    return edited_string
