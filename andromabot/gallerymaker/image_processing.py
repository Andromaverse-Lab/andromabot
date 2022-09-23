import asyncio
import logging
import os

from stargazeutils.ipfs import IpfsClient
from wand.image import Image

from .collections import AndromedaCollections

LOG = logging.getLogger(__name__)

IPFS_ROOT = os.environ.get("IPFS_ROOT", default="https://dweb.link")
ipfs = IpfsClient(ipfs_root=IPFS_ROOT)

ipfs_map = {
    AndromedaCollections.ANDROMA_PUNKS: {
        "ipfs": "bafybeie7f26w3jeqcmn4nj62sfae45nvl4ivg6fmk5gfmyybapcwlicica",
        "image_dir": "./images/collections/androma-punks",
        "logo": Image(filename="./images/apunks-logo.png"),
        "max_token": 270,
    },
    AndromedaCollections.ANDROMAVERSE: {
        "ipfs": "bafybeifhapzqtpmkazo7567mdyhn4fxla5hxho3xpy7qtxezzoz5zd7rsi",
        "image_dir": "./images/collections/andromaverse",
        "logo": Image(filename="./images/andromaverse-logo.png"),
        "max_token": 888,
    },
    AndromedaCollections.STARGAZE_PUNKS: {
        "ipfs": "bafybeicvvfnlxuo3ineufnwqcjvwvo64dkazv5an4lclrymb77fmnga2ze",
        "image_dir": "./images/collections/stargaze-punks",
        "logo": Image(filename="./images/spunks-logo.png"),
        "max_token": 8888,
    },
    AndromedaCollections.FORGOTTEN: {
        "ipfs": "bafybeibpdyyamxcw22wkih7d4of63y66eixnbo7gua7srkuls76fm7qlm4",
        "image_dir": "./images/collections/the-forgotten-punks",
        "logo": Image(filename="./images/forgotten-logo.png"),
        "max_token": 3456,
    },
}


async def get_image(collection: AndromedaCollections, token_id: int):
    c_info = ipfs_map[collection]

    if token_id > c_info["max_token"]:
        raise IndexError(
            f"{collection.name} only has {c_info['max_token']} tokens. "
            f"You requested #{token_id}."
        )

    image_path = f"{c_info['image_dir']}/{token_id}.png"
    if not os.path.exists(image_path):
        raise OSError(f"Unable to locate {collection.name} #{token_id}")

    return Image(filename=image_path)


async def create_gallery(tokens):
    bg = Image(filename="./images/gallery-bg.png")
    top = 380
    op = "dissolve"

    async def add_image(token, left):
        name = token["name"]
        id = token["id"]
        print(f"Adding image {name} {id}")
        image = await get_image(name, token["id"])

        bg.composite_channel("1", image, op, left, top)
        bg.composite_channel("1", ipfs_map[name]["logo"], op, left, top - 55)

    tasks = [
        add_image(tokens[0], 40),
        add_image(tokens[1], 427),
        add_image(tokens[2], 815),
        add_image(tokens[3], 1202),
    ]
    await asyncio.gather(*tasks)

    return bg
