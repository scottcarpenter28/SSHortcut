import json
import os
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel


class DatabaseConnection(BaseModel):
    connection: str = "sqlite+pysqlite:///:memory:"
    echo: bool = False


class Config(BaseModel):
    database: DatabaseConnection


def get_config_dir() -> Path:
    """
    Creates a path where the config file lives.
    :return: The path to the config file.
    """
    if os.name == "nt":  # Windows
        return Path(os.getenv("APPDATA")) / "SSHortcut"
    else:  # macOS/Linux
        return Path.home() / ".config" / "SSHortcut"


def create_default_config(path) -> None:
    """
    Creates the default config file.
    :param path: Path to the config file.
    :return: None
    """
    db_storage = path.parent.joinpath("default_storage.db")
    config = Config(
        database=DatabaseConnection(
            connection=f"sqlite+pysqlite:///{str(db_storage)}",
        )
    )
    with open(path, "w") as f:
        f.write(config.model_dump_json())


def load_or_create_config() -> Config:
    """
    Loads in the config file or creates one if one does not exist.
    :return: The configuration loaded into a dictionary.
    """
    config_dir = get_config_dir()
    config_path = config_dir / "config.yaml"

    if not config_dir.exists():
        config_dir.mkdir(parents=True)

    if not config_path.exists():
        create_default_config(config_path)

    with open(config_path, "r") as f:
        return Config(**json.loads(f.read()))
