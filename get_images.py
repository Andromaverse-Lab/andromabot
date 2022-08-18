import os
from wand.image import Image

def minify(src_dir, dst_dir, size):
    for file in os.listdir(src_dir):
        print(f"Minifying {src_dir}/{file}")
        image = Image(filename=os.path.join(src_dir,file))
        image.resize(size, size)
        image.save(filename=os.path.join(dst_dir, file))

minify("./images/collections-full/andromaverse", "./images/collections-sm/andromaverse", 300)
minify("./images/collections-full/stargaze-punks", "./images/collections-sm/stargaze-punks", 300)
