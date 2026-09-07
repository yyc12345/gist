from pathlib import Path

CMD_PATH_TRANS_TABLE: dict = str.maketrans(
    {
        '"': '\\"',  # escape double quote
        "\\": "\\\\",  # escape back slash
    }
)
"""Translation table for escape path for Windows cmd arguments"""


def safe_wrap_cmd_path(val: Path) -> str:
    """Escape path for Windows cmd arguments"""
    return f'"{str(val).translate(CMD_PATH_TRANS_TABLE)}"'


FILENAME_TRANS_TABLE: dict = str.maketrans(
    {
        # File system disallowed
        "\\": "",
        "/": "",
        ":": "",
        "*": "",
        "?": "",
        '"': "",
        "<": "",
        ">": "",
        "|": "",
    }
)


def sanitize_name(name: str) -> str:
    """Sanitize arbitary name to make it suit for file name."""
    return name.translate(FILENAME_TRANS_TABLE)
