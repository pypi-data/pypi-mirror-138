"""Help, usage and other texts / messages."""

import os


help_: dict = dict()
success: dict = dict()
usage: dict = dict()
description: dict = dict()

def register(to: object) -> object:
    """Register a class to option group [to]."""
    def wrapper(cls: object) -> object:
        try:
            to[cls.language]: object = cls
        except AttributeError:
            raise AttributeError(f"Option class should contain language attribute")
        return cls
    return wrapper


class OptionAdder:
    """Represents a base class for adding new options."""

    def add_option(self) -> None:
        """Adds new option."""


class HelpOption:
    """Represents a help option for options -h and --help."""

    def __init__(self) -> None:
        """Initialize and set up the help producer."""
        self.language: str = os.environ["LANG"]
        self.help: object = help_.get(self.language, EnglishHelp)()

    def __call__(self) -> None:
        """Make HelpOption callable."""
        self.help.print()


class Help:
    """Represents a base class for -h and --options."""

    def print(self) -> None:
        """Produces help."""


@register(help_)
class FinnishHelp(Help):

    language: str = "fi_FI.UTF-8"

    def print(self) -> None:
        """Produce help in Finnish."""
        print("Tämä on apuviesti.")


@register(help_)
class EnglishHelp(Help):

    language: str = "en_US.UTF-8"

    def print(self) -> None:
        """Produce help in English."""
        print("This is a help message.")


if __name__ == "__main__":
    print("Available help producers:")
    for _ in help_.items():
        print(_)
