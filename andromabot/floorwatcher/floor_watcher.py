import asyncio
import logging
from typing import List

import discord
from discord.activity import ActivityType

from ..config.config import CollectionConfig
from ..stargaze import fetch_trait_asks
from .floor_flow import FloorFlow

LOG = logging.getLogger(__name__)


def get_trend_emoji(x: List[int]) -> str:
    if x[-1] == 0:
        return "•"
    if x[0] > x[-1]:
        return "↗️"
    elif x[0] == x[-1]:
        return "➡️"
    return "↘️"


def get_min_ask(trait_asks: dict):
    def asking_price(x):
        return x["ask"].price.amount

    return min(
        [
            min(
                [
                    min(value_asks, key=asking_price)
                    for value_asks in trait_value.values()
                ],
                key=asking_price,
            )
            for trait_value in trait_asks.values()
        ],
        key=asking_price,
    )


class FloorWatcher:
    def __init__(self, client: discord.Client, collections: List[CollectionConfig]):
        self.client = client
        self.collections = collections
        self.latest_asks = {}
        self.floors = {}

        for c in self.collections:
            self.floors[c.name] = [0, 0, 0, 0, 0]

        list_collections_cmd = discord.app_commands.Command(
            name="listcollections",
            description="List tracked Stargaze collections with their floor price",
            callback=self.list_collections,
        )
        self.client.tree.add_command(list_collections_cmd)

        query_floor_cmd = discord.app_commands.Command(
            name="querytraitfloor",
            description="Query the floor pricing for a specific trait",
            callback=self.query_trait_floor,
        )
        self.client.tree.add_command(query_floor_cmd)

    async def begin_watching(self):
        self.bg_tasks = []
        for collection in self.collections:
            for channel in collection.channels:
                channel.guild = self.client.get_guild(channel.guild_id)
                channel.channel = self.client.get_channel(channel.channel_id)

            task = self.client.loop.create_task(self.track_floor_pricing(collection))
            self.bg_tasks.append(task)

    async def update_floor(self, collection: CollectionConfig):
        name = collection.name
        floor_history = self.floors[name]
        floor = floor_history[0]
        trend_emoji = get_trend_emoji(floor_history)

        LOG.info(f"{name} history: {[str(x) for x in floor_history]}")
        for ch in collection.channels:
            await ch.channel.edit(name=f"{collection.prefix}{floor:,} {trend_emoji}")

    async def update_asks(self, collection: CollectionConfig):
        name = collection.name
        activity = discord.Activity(type=ActivityType.watching, name="the stars 🌌🔭")
        await self.client.change_presence(activity=activity)

        LOG.info(f"Updating asks for '{name}'")
        trait_asks = fetch_trait_asks(name, collection.strict_validation)
        collection_floor = get_min_ask(trait_asks)

        if collection.enable_trait_query:
            self.latest_asks[name] = trait_asks
        new_floor = collection_floor["ask"].price.get_stars()
        self.floors[name].insert(0, new_floor)
        self.floors[name].pop()
        LOG.info(f"Finished updating asks for '{name}'")

        await self.client.change_presence(activity=None)

    async def track_floor_pricing(self, collection: CollectionConfig):
        interval = collection.refresh_interval

        while True:
            await self.update_asks(collection)
            LOG.info("Waiting until ready...")
            await self.client.wait_until_ready()
            await self.update_floor(collection)
            LOG.info(f"Refreshing {collection.name} in {interval} seconds")
            await asyncio.sleep(interval)

    async def list_collections(self, interaction: discord.Interaction):
        """List the currently tracked collections."""
        message = "**Tracked collections**\n"
        for collection, floor in self.floors.items():
            message += f"- {collection}: ({floor[0]:,} $STARS)\n"
        await interaction.response.send_message(message)

    async def query_trait_floor(
        self,
        interaction: discord.Interaction,
    ):
        floor_flow = FloorFlow(self.latest_asks)
        await floor_flow.start(interaction)
