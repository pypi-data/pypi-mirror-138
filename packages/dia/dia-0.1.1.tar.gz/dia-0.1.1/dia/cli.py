#!/usr/bin/env python3
from datetime import date
from pathlib import Path

import click

from .data_types import Diary


DIARY_FILENAME = "diary.txt"


@click.group()
@click.version_option()
def cli():
    pass


@cli.command(help="Compare a previous backup to the parameters on a craft.")
@click.argument("task")
def log(task: str):
    diary_file = Path(DIARY_FILENAME)
    if diary_file.exists():
        with diary_file.open() as infile:
            diary = Diary.from_text(infile.read())
    else:
        diary = Diary(days={})

    diary.add_day(date.today(), task)
    with diary_file.open("w") as outfile:
        outfile.write(diary.render())
    click.echo("Added task.")


if __name__ == "__main__":
    cli()
