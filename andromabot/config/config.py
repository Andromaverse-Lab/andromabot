import logging
from typing import List

import yaml

from .collection_config import CollectionConfig

LOG = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self.log_level = "INFO"
        self.refresh_interval = 300
        self.strict_validation = False
        self.guilds: List[int] = []
        self.collections: List[CollectionConfig] = []

    def _set_value(self, key, values):
        if key in values:
            self.__dict__[key] = values[key]
        LOG.info(f"{key} = {self.__dict__[key]}")

    @classmethod
    def from_yaml(cls, yaml_file):
        LOG.info(f"Loading configuration from file {yaml_file}")

        with open(yaml_file) as f:
            values = yaml.safe_load(f)

        config = cls()
        config._set_value("log_level", values)
        config._set_value("refresh_interval", values)
        config._set_value("strict_validation", values)
        config._set_value("guilds", values)

        for c in values["collections"]:
            c_config = CollectionConfig.from_dict(
                c, config.refresh_interval, config.strict_validation
            )
            config.collections.append(c_config)

        return config
