"""Parse command line input."""

import os
import sys


options: dict = dict()
def register(cls: object) -> object:
    """
    Register class as option, using its method as callback.

    Class [cls] needs to define one of the following class variables:
    short or long. Class [cls] also needs to define a method named
    callback, that will be used as a callback.
    """

    if not any([hasattr(cls, "short"), hasattr(cls, "long")]):
        raise AttributeError("Option class must define at least short or long option")

    if not hasattr(cls, "callback"):
        raise AttributeError("Option class must define a callback method")

    if hasattr(cls, "short"):
        options[cls.short]: object = cls().callback

    if hasattr(cls, "long"):
        options[cls.long]: object = cls().callback

    return cls


@register
class HelpOption:

    short: str = None
    long: str = "--help"

    def callback(self) -> None:
        print("This is callback")


class ArgumentParser:
    """Represents argument parser for parsing sys.argv."""

    def __init__(self) -> None:
        """Set up program name, system language etc."""
        self.argv: list = sys.argv
        self.argc: int = len(sys.argv)
        self.program: str = self.argv[0]

        self._args: bool = self.argc >= 2
        self._help: bool = "--help" in self.argv or "-h" in self.argv
        self._version: bool = "--version" in self.argv or "-V" in self.argv
        self._config: bool = "--config" in self.argv or "-C" in self.argv

    def parse(self) -> None:
        """Execute option's callback if such is provided at the command line."""
        pass

    @property
    def args(self) -> bool:
        """
        Get whether sufficient number of arguments was provided
        on the command line.
        """
        return self._args

    @property
    def help(self) -> bool:
        """Get whether either -h or --help was provided on the command line."""
        return self._help

    @property
    def version(self) -> bool:
        """Get whether either -V or --version was provided on the command line."""
        return self._version

    @property
    def config(self) -> bool:
        """Get whether either -C or --config was provided on the command line."""
        return self._config


if __name__ == "__main__":
    pass
