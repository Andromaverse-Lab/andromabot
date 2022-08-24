#!/usr/bin/env python3

import sys
import asyncio
from andromabot.gallerymaker.image_processing import create_gallery
from andromabot.gallerymaker.collections import AndromedaCollections

names = sys.argv[1::2]
ids = sys.argv[2::2]
tokens = [{"name":AndromedaCollections.from_str(k),"id":int(v)} for k,v in zip(names,ids)]

loop = asyncio.new_event_loop()
gallery = loop.run_until_complete(create_gallery(tokens))
gallery.save(filename="gallery.png")
