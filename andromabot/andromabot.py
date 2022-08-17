import logging

import discord

from .config.config import Config
from .floorwatcher.floor_watcher import FloorWatcher
from .gallerymaker.gallery_maker import GalleryMaker

LOG = logging.getLogger(__name__)


class AndromaBot(discord.Client):
    def __init__(self, intents: discord.Intents, config: Config):
        super().__init__(intents=intents)
        self.config = config
        self.tree = discord.app_commands.CommandTree(self)

        self.floor_watcher = FloorWatcher(self, self.config.collections)
        self.gallery_maker = GalleryMaker(self)

    async def setup_hook(self) -> None:
        guild_ids = set()
        for c in self.config.collections:
            for channel in c.channels:
                guild_ids.add(channel.guild_id)

        for guild_id in guild_ids:
            guild = discord.Object(guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        LOG.info(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.floor_watcher.begin_watching()
