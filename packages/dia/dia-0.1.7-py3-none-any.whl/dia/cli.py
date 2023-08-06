#!/usr/bin/env python3
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import click
import click_config_file

from .data_types import Diary
from .utils import get_editor

DEFAULT_FILENAME = "diary.txt"
TOKEN_RE = r"""
    (?:\W+|^)    # Don't have stuff before the %.
    {}           # The token.
    (
    [\w\-\.]+    # Word stuff.
    \w           # The last character shouldn't be special.
    )
    """


@click.group()
@click.version_option()
@click.option(
    "--diary",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_FILENAME,
    help="Read/write the diary to FILE.",
)
@click.pass_context
@click_config_file.configuration_option()
def cli(ctx, diary: Path):
    class Context:
        def __init__(self):
            self.diary_file = diary
            self.diary = Diary(days={})

    ctx.obj = Context()
    if ctx.obj.diary_file.exists():
        with ctx.obj.diary_file.open() as infile:
            ctx.obj.diary = Diary.from_text(infile.read())


@cli.command(help="Produce a list of tasks suitable for an async standup.")
@click.argument("keyword", required=False)
@click.option(
    "-r",
    "--regex",
    is_flag=True,
    help="Treat KEYWORD as a regex.",
)
@click.pass_obj
def standup(obj, keyword: str, regex: bool):
    keyword = keyword if keyword else ""
    keyword = keyword if regex else re.escape(keyword)
    previous_day = obj.diary.previous_day().filter(re.compile(keyword, re.IGNORECASE))

    click.secho(previous_day.date.strftime("*%Y-%m-%d, %A:*"), fg="green")
    if previous_day.tasks:
        click.echo(
            (
                "\n"
                + "\n".join((task.render(colors=True)) for task in previous_day.tasks)
            ).strip()
        )
    else:
        click.echo(click.style("* ", fg="blue") + "Nothing relevant.")

    click.secho("\n*Today:*", fg="green")
    click.echo(click.style("* ", fg="blue") + "Nothing relevant.")

    click.secho("\n*Blockers:*", fg="green")
    click.echo(click.style("* ", fg="blue") + "None.")


@cli.command(help="Search for specific keywords (case-insensitive).")
@click.argument("keyword")
@click.option(
    "-r",
    "--regex",
    is_flag=True,
    help="Treat KEYWORD as a regex.",
)
@click.pass_obj
def search(obj, keyword: str, regex: bool):
    keyword = keyword if regex else re.escape(keyword)
    diary = obj.diary.filter(re.compile(keyword, re.IGNORECASE))
    click.echo(diary.render(colors=True))


@cli.group(help="Show all (or specific) tasks.", invoke_without_command=True)
@click.pass_context
@click.pass_obj
def show(obj, ctx):
    if ctx.invoked_subcommand:
        return
    click.echo_via_pager(obj.diary.render(colors=True))


@show.command(help="Show the previous day's tasks.")
@click.pass_obj
def previous(obj):
    # Compile all previous days.
    previous_day = obj.diary.previous_day()

    if not previous_day:
        sys.exit(click.style("No previous tasks.", fg="red"))
    click.echo("\n" + previous_day.render(colors=True) + "\n")


@show.command(help="Show today's tasks.")
@click.pass_obj
def today(obj):
    day = obj.diary.days.get(date.today())
    if not day:
        sys.exit(click.style("No tasks yet today.", fg="red"))
    click.echo("\n" + day.render(colors=True) + "\n")


@show.command(help="Show all projects.")
@click.pass_obj
def projects(obj):
    items = set(obj.diary.sift(re.compile(TOKEN_RE.format("%"), re.VERBOSE)))
    click.secho("Projects\n========", fg="green")
    click.echo("* " + ("\n* ".join(sorted(items))))


@show.command(help="Show all people.")
@click.pass_obj
def people(obj):
    items = set(obj.diary.sift(re.compile(TOKEN_RE.format("@"), re.VERBOSE)))
    click.secho("People\n======", fg="green")
    click.echo("* " + ("\n* ".join(sorted(items))))


@show.command(help="Show all tags.")
@click.pass_obj
def tags(obj):
    items = set(obj.diary.sift(re.compile(TOKEN_RE.format(r"\#"), re.VERBOSE)))
    click.secho("Tags\n====", fg="green")
    click.echo("* " + ("\n* ".join(sorted(items))))


@cli.command(help="Edit the diary in your default editor.")
@click.pass_context
def edit(ctx):
    subprocess.call([get_editor(), ctx.obj.diary_file])


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
