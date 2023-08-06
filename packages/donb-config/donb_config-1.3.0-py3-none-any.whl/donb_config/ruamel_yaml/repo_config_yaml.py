from __future__ import annotations

import dataclasses
import shutil
import sys
from fileinput import FileInput
from pathlib import Path
from typing import Optional, Any, Generic

from ruamel import yaml

from donb_config.base_class import ConfigBase
from donb_config.interface_repo_config import IRepoConfig
from donb_config.types import Config


class RepoConfigYaml(Generic[Config]):

    """
    ConfigYamlRepository implements both IConfigRepositoryLoader and
    IConfigRepositoryModifier. It uses ruamel.yaml and stores the configuration in a
    .yaml file.

    Ruamel.yaml allows to keep the comments and general formatting of the
    pre-existing .yaml file when saving new values. The actual data, including the
    information about the comments and formatting are stored in a private attribute
    _data.

    """

    def __init__(
        self,
        config_class: type[Config],
        config_folder_relative_path: Path,
        default_config_file_path: Path,
    ) -> None:
        self._config_class = config_class
        self._default_config_file_path = default_config_file_path
        self._config_file_path: Path = self._get_config_file_path(
            config_folder_relative_path
        )
        self._data: Optional[dict[str, Any]] = None
        assert isinstance(self, IRepoConfig)

    def load(self) -> Config:
        """See IConfigRepositoryLoader documentation."""
        if not self._config_file_path.exists():
            self._create_default_config_file()
        self._data = yaml.YAML().load(self._config_file_path)
        # Impossible for mypy to know how many arguments are expected
        try:
            config = self._config_class(**self._data)  # type: ignore [call-arg]
        except (TypeError, ValueError, KeyError):
            config = self._repair_and_fetch()
        return config

    def save(self, config: Config) -> None:
        """See IConfigRepositoryModifier documentation."""
        yaml_instance = yaml.YAML()
        # If self.data has not yet been initialized, the comments in the yaml file
        # would be lost if we simply dumped the values from config. So we load first,
        # modify the value, and then dump the data including all original comments.
        if not self._data:
            self.load()
        assert self._data is not None
        self._replace_values(self._data, config)
        yaml_instance.dump(self._data, self._config_file_path)
        # For some reason, in conditions that I haven't been able to define precisely,
        # dumping the new values adds blank lines after comments, which are removed
        # by the _format_file method.
        self._format_file()

    @staticmethod
    def _replace_values(data_dict: dict[str, Any], config: Config) -> None:
        for field in dataclasses.fields(config):
            value = getattr(config, field.name)
            if isinstance(value, ConfigBase):
                RepoConfigYaml._replace_values(data_dict[field.name], value)
            elif isinstance(value, Path):
                data_dict[field.name] = str(value.absolute())
            else:
                data_dict[field.name] = value

    @staticmethod
    def _get_config_file_path(config_folder_relative_path: Path) -> Path:
        home_directory = Path.home()
        is_win32 = "win32" in str(sys.platform).lower()
        if is_win32:
            config_directory = (
                home_directory / "AppData" / "Roaming" / config_folder_relative_path
            )
        elif config_folder_relative_path.parts[0].startswith("."):
            config_directory = home_directory / config_folder_relative_path
        else:
            config_directory = (
                home_directory
                / ("." + config_folder_relative_path.parts[0])
                / Path(*config_folder_relative_path.parts[1:])
            )
        my_config_file_path = config_directory / "config.yaml"
        return my_config_file_path

    def _create_default_config_file(self) -> None:
        config_folder = self._config_file_path.parent
        config_folder.mkdir(parents=True, exist_ok=True)
        shutil.copy(self._default_config_file_path, self._config_file_path)

    def _repair_and_fetch(self) -> Config:
        yaml_instance = yaml.YAML()
        corrupted_data = yaml_instance.load(self._config_file_path)
        self._create_default_config_file()
        self._data = yaml_instance.load(self._config_file_path)
        assert self._data is not None
        if corrupted_data:
            self._repair_dict(self._data, corrupted_data)
        # Impossible for mypy to know how many arguments are expected
        config = self._config_class(**self._data)  # type: ignore [call-arg]
        self.save(config)
        return config

    @staticmethod
    def _repair_dict(new_dict: dict[str, Any], corrupted_dict: dict[str, Any]) -> None:
        for key in new_dict:
            if isinstance(new_dict[key], yaml.comments.CommentedMap) and isinstance(
                corrupted_dict[key], yaml.comments.CommentedMap
            ):
                RepoConfigYaml._repair_dict(new_dict[key], corrupted_dict[key])
            elif not isinstance(new_dict[key], yaml.comments.CommentedMap):
                RepoConfigYaml._repair_value(new_dict, corrupted_dict, key)

    @staticmethod
    def _repair_value(
        new_dict: dict[str, Any], corrupted_dict: dict[str, Any], key: str
    ) -> None:
        new_type = type(new_dict[key])
        try:
            new_dict[key] = new_type(corrupted_dict[key])
        except (KeyError, TypeError):
            pass

    def _format_file(self) -> None:
        self._remove_blank_lines()
        self._add_blank_lines_between_sections()

    def _remove_blank_lines(self) -> None:
        with FileInput(self._config_file_path, inplace=True) as config_file:
            for line in config_file:
                if line != "\n":
                    print(line, end="")

    def _add_blank_lines_between_sections(self) -> None:
        with FileInput(self._config_file_path, inplace=True) as config_file:
            first_line = True
            for line in config_file:
                if line.startswith("#") and not first_line:
                    print("\n", end="")
                first_line = False
                print(line, end="")
