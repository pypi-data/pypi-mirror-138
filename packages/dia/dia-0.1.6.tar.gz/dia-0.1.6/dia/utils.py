import click


def style(text: str, fg: str, colors: bool = False):
    """Style a string only if `colors` is `True`."""
    if not colors:
        return text
    return click.style(text, fg=fg)
