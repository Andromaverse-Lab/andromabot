import asyncio
import logging
import os

import aiohttp
from stargazeutils.ipfs import IpfsClient
from wand.image import Image

from .collections import AndromedaCollections

LOG = logging.getLogger(__name__)

IPFS_ROOT = os.environ.get("IPFS_ROOT", default="https://dweb.link")
ipfs = IpfsClient(ipfs_root=IPFS_ROOT)

ipfs_map = {
    AndromedaCollections.ANDROMA_PUNKS: {
        "ipfs": "bafybeie7f26w3jeqcmn4nj62sfae45nvl4ivg6fmk5gfmyybapcwlicica",
        "logo": "./images/apunks-logo.png",
        "max_token": 270,
    },
    AndromedaCollections.ANDROMAVERSE: {
        "ipfs": "bafybeifhapzqtpmkazo7567mdyhn4fxla5hxho3xpy7qtxezzoz5zd7rsi",
        "logo": "./images/andromaverse-logo.png",
        "max_token": 888,
    },
    AndromedaCollections.STARGAZE_PUNKS: {
        "ipfs": "bafybeicvvfnlxuo3ineufnwqcjvwvo64dkazv5an4lclrymb77fmnga2ze",
        "logo": "./images/spunks-logo.png",
        "max_token": 8888,
    },
}

for k, v in ipfs_map.items():
    logo = Image(filename=v["logo"])
    logo.resize(300, 30)
    ipfs_map[k]["logo_img"] = logo


async def get_image(
    session: aiohttp.ClientSession, collection: AndromedaCollections, token_id: int
):
    c_info = ipfs_map[collection]
    if token_id > c_info["max_token"]:
        raise IndexError(
            f"{collection.name} only has {c_info['max_token']} tokens. "
            f"You requested #{token_id}."
        )
    ipfs_url = f"ipfs://{c_info['ipfs']}/images/{token_id}.png"
    image_url = ipfs.ipfs_to_http(ipfs_url)
    async with session.get(image_url) as response:
        if response.status != 200:
            LOG.warning(
                f"Unable to fetch {collection.name} {token_id} status {response.status}"
            )
            LOG.warning(f"Url = {image_url}")
            return Image()
        data = await response.content.read()
        image = Image(blob=data)
    return image


async def create_gallery(tokens):
    bg = Image(filename="./images/gallery-bg.png")
    frame_w, frame_h = 300, 300
    top = 380

    async def add_image(session, token, left):
        name = token["name"]
        id = token["id"]
        print(f"Adding image {name} {id}")
        image = await get_image(session, name, token["id"])
        image.resize(frame_w, frame_h)
        bg.composite_channel("all_channels", image, "dissolve", left, top)
        bg.composite_channel(
            "all_channels", ipfs_map[name]["logo_img"], "dissolve", left, top - 55
        )

    async with aiohttp.ClientSession() as session:
        tasks = [
            add_image(session, tokens[0], 40),
            add_image(session, tokens[1], 427),
            add_image(session, tokens[2], 815),
            add_image(session, tokens[3], 1202),
        ]
        await asyncio.gather(*tasks)

    return bg
