import os
import shutil

import click


def style(text: str, fg: str, colors: bool = False):
    """Style a string only if `colors` is `True`."""
    if not colors:
        return text
    return click.style(text, fg=fg)


def get_editor() -> str:
    """Get the default editor in the system."""
    editor = (
        shutil.which("editor") or os.getenv("VISUAL") or os.getenv("EDITOR") or "vi"
    )
    return editor
