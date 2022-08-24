import logging

import discord
from discord.activity import ActivityType

from .collections import AndromedaCollections
from .image_processing import create_gallery

LOG = logging.getLogger(__name__)


class GalleryMaker:
    def __init__(self, client: discord.Client):
        self.client = client

        create_gallery_cmd = discord.app_commands.Command(
            name="create-gallery",
            description="Creates a gallery of 4 Andromeda Labs tokens",
            callback=self.create_gallery,
        )
        self.client.tree.add_command(create_gallery_cmd)

    @discord.app_commands.describe(
        collection_1="First image's collection",
        token_1="First image's token id",
        collection_2="Second image's collection",
        token_2="Second image's token id",
        collection_3="Third image's collection",
        token_3="Third image's token id",
        collection_4="Fourth image's collection",
        token_4="Fourth image's token id",
    )
    async def create_gallery(
        self,
        interaction: discord.Interaction,
        collection_1: AndromedaCollections,
        token_1: int,
        collection_2: AndromedaCollections,
        token_2: int,
        collection_3: AndromedaCollections,
        token_3: int,
        collection_4: AndromedaCollections,
        token_4: int,
    ):
        """Creates a gallery of 4 Andromeda Labs tokens."""
        tokens = [
            {"name": collection_1, "id": token_1},
            {"name": collection_2, "id": token_2},
            {"name": collection_3, "id": token_3},
            {"name": collection_4, "id": token_4},
        ]

        LOG.info("Received request")
        await interaction.response.defer(thinking=True)

        activity = discord.Activity(type=ActivityType.playing, name="The Gallerist 🖼")
        await self.client.change_presence(activity=activity)
        try:
            gallery = await create_gallery(tokens)
            filename = "gallery.png"
            gallery.save(filename=filename)
            file = discord.File(filename)
            await interaction.followup.send(file=file)
        except (IndexError, OSError) as e:
            await interaction.followup.send(e)
        await self.client.change_presence(activity=None)
