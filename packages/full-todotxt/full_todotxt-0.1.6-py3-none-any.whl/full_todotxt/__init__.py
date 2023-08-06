#!/usr/bin/env python3

import os
import re

from datetime import datetime, date
from typing import Union, List, Set, Optional
from pathlib import Path
from shutil import copyfile

import click

from pytodotxt.todotxt import TodoTxt, Task
import dateparser

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, input_dialog, button_dialog
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.formatted_text import HTML

PathIsh = Union[Path, str]


class ProjectTagValidator(Validator):
    def validate(self, document):
        text = document.text

        if len(text.strip()) == 0:
            raise ValidationError(message="You must specify at least one project tag")

        # check if all input matches '+projectag'
        for project_tag in text.split():
            if not bool(re.match("\+\w+", project_tag)):
                raise ValidationError(
                    message=f"'{project_tag}' doesn't look like a project tag. e.g. '+home'"
                )


# global tag information
ALL_TAGS: Set[str] = set()


# prompt the user to add a todo
def prompt_todo(add_due: bool, time_format: str) -> Optional[Task]:

    # prompt the user for a new todo (just the text)
    todo_text: Optional[str] = input_dialog(title="Add Todo:").run()

    if todo_text is None:
        return None
    elif not todo_text.strip():
        message_dialog(title="Error", text="No input provided for the todo").run()
        return None

    # project tags
    print("Enter one or more tags, hit 'Tab' to autocomplete")
    projects_raw: str = prompt(
        "[Enter Project Tags]> ",
        completer=FuzzyWordCompleter(list(ALL_TAGS)),
        complete_while_typing=True,
        validator=ProjectTagValidator(),
        bottom_toolbar=HTML("<b>Todo:</b> {}".format(todo_text)),
    )

    # select priority
    todo_priority: str = button_dialog(
        title="Priority:",
        text="A is highest, C is lowest",
        buttons=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
        ],
    ).run()

    # ask if the user wants to add a time
    add_time: bool = button_dialog(
        title="Deadline:",
        text="Do you want to add a deadline for this todo?",
        buttons=[
            ("No", False),
            ("Yes", True),
        ],
    ).run()

    # prompt for adding a deadline
    todo_time: Optional[datetime] = None
    if add_time:
        while todo_time is None:
            todo_time_str: Optional[str] = input_dialog(
                title="Describe the deadline.",
                text="For example:\n'9AM', 'noon', 'tomorrow at 10PM', 'may 30th at 8PM'",
            ).run()
            # if user hit cancel
            if todo_time_str is None:
                add_time = False
                break
            else:
                todo_time = dateparser.parse(
                    todo_time_str, settings={"PREFER_DATES_FROM": "future"}
                )
                if todo_time is None:
                    message_dialog(
                        title="Error",
                        text="Could not parse '{}' into datetime".format(todo_time_str),
                    ).run()

    # construct the TODO
    constructed: str = f"({todo_priority})"
    constructed += f" {date.today()}"
    constructed += f" {todo_text}"
    constructed += f" {projects_raw}"
    if todo_time is not None:
        constructed += f" deadline:{datetime.strftime(todo_time, time_format)}"
        if add_due:
            constructed += f" due:{datetime.strftime(todo_time, r'%Y-%m-%d')}"

    t = Task(constructed)
    return t


def full_backup(todotxt_file: PathIsh) -> None:
    """
    Backs up the todo.txt file before writing to it
    """
    backup_file: PathIsh = f"{todotxt_file}.full.bak"
    copyfile(str(todotxt_file), str(backup_file))


def parse_projects(todo_sources: List[TodoTxt]) -> None:
    """Get a list of all tags from the todos"""
    global ALL_TAGS
    for tf in todo_sources:
        for todo in tf.tasks:
            for proj in todo.projects:
                ALL_TAGS.add(f"+{proj}")


def locate_todotxt_file(todotxt_filepath: Optional[Path]) -> Optional[PathIsh]:
    if todotxt_filepath is not None:
        if not os.path.exists(todotxt_filepath):
            click.echo(
                f"The provided file '{todotxt_filepath}' does not exist.", err=True
            )
            return None
        else:
            return todotxt_filepath
    else:  # no todo file passed, test some common locations
        home: PathIsh = Path.home()
        possible_locations = [
            os.path.join(home, ".config/todo/todo.txt"),
            os.path.join(home, ".todo/todo.txt"),
        ]
        if "TODO_DIR" in os.environ:
            possible_locations.insert(
                0, os.path.join(os.environ["TODO_DIR"], "todo.txt")
            )
        for p in possible_locations:
            if os.path.exists(p):
                click.echo(f"Found todo.txt file at {p}, using...")
                return p
        else:
            return None


@click.command()
@click.argument(
    "todotxt-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    required=False,
)
@click.option(
    "--add-due/--no-add-due",
    is_flag=True,
    default=False,
    help="Add due: key/value flag based on deadline:",
    show_default=True,
)
@click.option(
    "--time-format",
    default="%Y-%m-%d-%H-%M",
    show_default=True,
    help="Specify a different time format for deadline:",
)
def cli(todotxt_file: Optional[Path], add_due: bool, time_format: str):

    # handle argument
    tfile = locate_todotxt_file(todotxt_file)
    if tfile is None:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    # read from main todo.txt file
    todos: TodoTxt = TodoTxt(tfile)

    # backup todo.txt file
    full_backup(tfile)

    # list of sources, done.txt will be added if it exists
    todo_sources: List[TodoTxt] = [todos]

    done_file: PathIsh = os.path.join(os.path.dirname(tfile), "done.txt")
    if not os.path.exists(done_file):
        click.secho(
            f"Could not find the done.txt file at {done_file}", err=True, fg="red"
        )
    else:
        todo_sources.append(TodoTxt(done_file))

    for t in todo_sources:
        t.parse()

    # parse a list of all tags from the todo.txt/done.txt file
    parse_projects(todo_sources)

    # prompt user for new todo
    new_todo: Optional[Task] = prompt_todo(add_due, time_format)

    # write back to file
    if new_todo is not None:
        todos.tasks.append(new_todo)
        click.echo(
            "{}: {}".format(click.style("Adding Todo", fg="green"), str(new_todo))
        )
        todos.save(safe=True)
