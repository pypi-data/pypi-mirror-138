#!/usr/bin/env python3
from datetime import date
from pathlib import Path

import click

from .data_types import Diary


DIARY_FILENAME = "diary.txt"


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    # Create a dummy class.
    ctx.obj = type("obj", (), {})
    ctx.obj.diary_file = Path(DIARY_FILENAME)
    if ctx.obj.diary_file.exists():
        with ctx.obj.diary_file.open() as infile:
            ctx.obj.diary = Diary.from_text(infile.read())
    else:
        ctx.obj.diary = Diary(days={})


@cli.command(help="Show today's tasks.")
@click.pass_obj
def today(obj):
    day = obj.diary.days.get(date.today())
    click.echo("\n" + day.render(colors=True))


@cli.command(help="Add another task to today's section.")
@click.argument("task")
@click.pass_context
def log(ctx, task: str):
    ctx.obj.diary.add_day(date.today(), task)
    with ctx.obj.diary_file.open("w") as outfile:
        outfile.write(ctx.obj.diary.render())
    ctx.invoke(today)


if __name__ == "__main__":
    cli()
