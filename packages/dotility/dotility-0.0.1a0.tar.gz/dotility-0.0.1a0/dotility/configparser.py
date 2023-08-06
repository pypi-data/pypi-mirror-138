"""Parser for Relieve's config file."""

import pathlib

import ruamel.yaml


class Config:
    """Represents a set of settings about Relieve's config."""

    def __init__(self) -> None:
        """Initialize where to read and write config to."""
        self.path: str = "".join([str(pathlib.Path.home()), "/.config/relieve"])


class ConfigWriter(Config):
    """Represents a writer that writes the default configuration for Relieve."""

    def __init__(self) -> None:
        """Initialize ConfigWriter for writing."""
        super().__init__()
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)


class ConfigParser(Config):
    """Represents a config parser for parsing Relieve's config file(s)."""

    def __init__(self) -> None:
        """Initialize a reader for parsing config."""
        super().__init__()
        self.yaml: object = ruamel.yaml.YAML()
