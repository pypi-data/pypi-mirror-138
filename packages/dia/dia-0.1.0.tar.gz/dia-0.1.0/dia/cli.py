#!/usr/bin/env python3
from datetime import date

import click

from .data_types import Diary


DIARY_FILENAME = "log.txt"


@click.group()
@click.version_option()
def cli():
    pass


@cli.command(help="Compare a previous backup to the parameters on a craft.")
@click.argument("task")
def log(task: str):
    with open(DIARY_FILENAME) as infile:
        diary = Diary.from_text(infile.read())
    diary.add_day(date.today(), task)
    with open(DIARY_FILENAME, "w") as outfile:
        outfile.write(diary.render())
    click.echo("Added task.")


if __name__ == "__main__":
    cli()
