from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Generic
from pathlib import Path

from donb_config.base_class import ConfigBase
from donb_config.ruamel_yaml import RepoConfigYaml
from donb_config.types import Config

if TYPE_CHECKING:
    from donb_config.interface_repo_config import IRepoConfig


_dict_suffix_class: dict[str, type[IRepoConfig]] = {"yaml": RepoConfigYaml}


class ConfigManager(Generic[Config]):
    def __init__(
        self,
        config_class: type[Config],
        config_folder_relative_path: Path,
        default_config_file_path: Path,
    ):
        assert issubclass(config_class, ConfigBase)
        self._repo_config_class = self._get_repo_class_from_suffix(
            default_config_file_path
        )
        self._repo_config = self._repo_config_class(
            config_class, config_folder_relative_path, default_config_file_path
        )
        self._config: Optional[Config] = None

    @property
    def config_instance(self) -> Config:
        if self._config is None:
            self._config = self._repo_config.load()
        return self._config

    def save(self, config: Config) -> None:
        self._repo_config.save(config)

    @staticmethod
    def _get_repo_class_from_suffix(
        default_config_file_path: Path,
    ) -> type[IRepoConfig]:
        config_file_suffix = default_config_file_path.name.split(".")[-1]
        try:
            repo_config_class = _dict_suffix_class[config_file_suffix]
        except KeyError as err:
            raise KeyError(
                "Extension de fichier de configuration non pris en charge"
            ) from err
        return repo_config_class
