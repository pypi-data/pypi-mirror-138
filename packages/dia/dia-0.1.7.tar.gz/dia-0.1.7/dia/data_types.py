import datetime
import re
import textwrap
from dataclasses import dataclass
from datetime import date
from typing import Dict
from typing import List
from typing import Optional

from .utils import style


@dataclass(order=True, eq=True)
class Task:
    text: str

    def render(self, colors: bool = False) -> str:
        """Render a task into Markdown."""
        return style("* ", fg="blue", colors=colors) + "\n  ".join(
            textwrap.wrap(self.text, width=86)
        )


@dataclass(order=True, eq=True)
class Day:
    date: datetime.date
    tasks: List[Task]

    def add_task(self, text: str):
        self.tasks.append(Task(text=text))

    def render(self, colors=False) -> str:
        current_date = self.date.strftime("%Y-%m-%d, %A")
        return (
            style(current_date, fg="green", colors=colors)
            + "\n"
            + style("-" * len(current_date), fg="green", colors=colors)
            + "\n"
            + "\n".join((task.render(colors=colors)) for task in self.tasks)
        ).strip()

    def filter(self, regex: re.Pattern) -> "Day":
        """
        Filter tasks by a regex.

        Returns a new (potentially empty) Day instance.
        """
        new_day = Day(
            date=self.date,
            tasks=[task for task in self.tasks if regex.search(task.text)],
        )
        return new_day


@dataclass(order=True, eq=True)
class Diary:
    days: Dict[datetime.date, Day]

    def render(self, colors=False) -> str:
        text = [
            style("Work diary", fg="blue", colors=colors),
            style("==========\n", fg="blue", colors=colors),
        ]
        if not self.days:
            text.append("No tasks yet.")
        else:
            for day in sorted(self.days.values(), reverse=True):
                text.append(day.render(colors=colors) + "\n")
        return "\n".join(text).strip()

    def sift(self, regex: re.Pattern) -> List[str]:
        """Return all regex matches in all tasks."""
        matches = []
        for day in self.days.values():
            for task in day.tasks:
                matches.extend(regex.findall(task.text))
        return matches

    def previous_day(self) -> Optional[Day]:
        """Return the day previous to today."""
        # Compile all previous days.
        previous_day = None
        for day in sorted(self.days.values(), reverse=True):
            if day.date < date.today():
                previous_day = day
                break
        return previous_day

    @property
    def tasks(self) -> List[Task]:
        """
        Return a flat list of all tasks in the diary.

        Flattens the diary into a list of tasks.
        """
        tasks = []
        for day in sorted(self.days.values()):
            tasks.extend(day.tasks)
        return tasks

    def filter(self, regex: re.Pattern) -> "Diary":
        """
        Filter tasks by a regex.

        Returns a new Diary instance with only the days that contain at least one task.
        """
        new_diary = Diary(days={})
        for day_date, day in self.days.items():
            new_day = day.filter(regex)
            if new_day.tasks:
                new_diary.days[day_date] = new_day
        return new_diary

    def add_day(self, date: datetime.date, text: str) -> None:
        """Add a task to the diary."""
        day = self.days.get(date, Day(date=date, tasks=[]))
        day.add_task(text)
        self.days[date] = day

    @classmethod
    def from_text(cls, text: str) -> "Diary":
        """
        Parse a log file and return a Diary object from it.

        This function is a bit heavy, because it does actual text parsing, but eh,
        should be ok.
        """
        # Add a date to the end of the text, so that we correctly parse the last day
        # when the file ends.
        text += "\n1000-01-01"

        DATE_RE = re.compile(r"^\w*(\d{4}-\d{2}-\d{2})\w*")
        TASK_RE = re.compile(r"^\* (.*)$")

        days: Dict[datetime.date, Day] = {}
        day_tasks = []
        day_date = datetime.date(1000, 1, 1)
        task: List[str] = []
        for line in text.split("\n"):
            if DATE_RE.search(line) or TASK_RE.search(line):
                # A task ended.
                if task:
                    day_tasks.append(Task(text=" ".join(task)))
                task = []

            if match := DATE_RE.search(line):
                # A new day begins.
                task = []
                if day_tasks:
                    days[day_date] = Day(date=day_date, tasks=day_tasks)
                    day_tasks = []
                day_date = datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
            elif match := TASK_RE.search(line):
                # A new task begins.
                task.append(match.group(1))
            elif task and line.startswith("  "):
                # A task continues.
                text = line[2:]
                if text:
                    task.append(text)

        diary = cls(days=days)
        return diary
