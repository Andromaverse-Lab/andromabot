import logging
import os

import discord

from .andromabot import AndromaBot
from .config.config import Config

logging.basicConfig(level=logging.INFO)
CONFIG_FILE = os.environ.get("CONFIG_FILE", default="config.yaml")
config = Config.from_yaml(CONFIG_FILE)

DISCORD_KEY = os.environ.get("DISCORD_KEY")

logging.basicConfig(level=logging._nameToLevel[config.log_level])
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("stargazeutils.market.market_client").setLevel(logging.WARNING)
logging.getLogger("stargazeutils.market.market_ask").setLevel(logging.ERROR)
LOG = logging.getLogger(__name__)

intents = discord.Intents.default()
client = AndromaBot(intents, config)
client.run(DISCORD_KEY)

# https://canary.discord.com/channels/977279710713245766/
