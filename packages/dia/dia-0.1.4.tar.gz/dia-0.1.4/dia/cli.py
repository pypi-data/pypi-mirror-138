#!/usr/bin/env python3
from datetime import date
from pathlib import Path

import click
import click_config_file

from .data_types import Diary


@click.group()
@click.version_option()
@click.option(
    "--diary",
    "diary_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default="diary.txt",
    help="Read/write the diary to FILE.",
)
@click.pass_context
@click_config_file.configuration_option()
def cli(ctx, diary_path: Path):
    class Context:
        diary_file = diary_path
        diary = Diary(days={})

    ctx.obj = Context()
    if ctx.obj.diary_file.exists():
        with ctx.obj.diary_file.open() as infile:
            ctx.obj.diary = Diary.from_text(infile.read())


@cli.command(help="Show all tasks.")
@click.pass_obj
def show(obj):
    click.echo_via_pager(obj.diary.render(colors=True))


@cli.command(help="Show today's tasks.")
@click.pass_obj
def today(obj):
    day = obj.diary.days.get(date.today())
    click.echo("\n" + day.render(colors=True) + "\n")


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
