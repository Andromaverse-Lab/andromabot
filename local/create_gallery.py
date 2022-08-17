#!/usr/bin/env python3

import sys
from gallerymaker.gallery import create_gallery
from gallerymaker.collections import AndromedaCollections

names = sys.argv[1::2]
ids = sys.argv[2::2]
tokens = [{"name":AndromedaCollections.from_str(k),"id":v} for k,v in zip(names,ids)]

gallery = create_gallery(tokens)
gallery.save(filename="gallery.png")
