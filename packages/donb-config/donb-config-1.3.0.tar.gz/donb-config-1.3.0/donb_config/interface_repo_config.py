# -*- coding: utf-8 -*-

"""
Defines the ConfigProvider class, and the IConfigRepositoryProtocol.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable, Generic

from donb_config.types import Config


@runtime_checkable
class IRepoConfig(Protocol, Generic[Config]):

    """
    IConfigRepository is the protocol that must be implemented by a concrete
    implementation of any configuration file repository.
    """

    def __init__(  # pylint: disable=super-init-not-called
        self,
        type_config: type[Config],
        config_folder_relative_path: Path,
        default_config_file_path: Path,
    ) -> None:
        ...

    def load(self) -> Config:
        """
        Loads data from the configuration repository and returns the corresponding
        Config object.
        """

    def save(self, config: Config) -> None:
        ...
