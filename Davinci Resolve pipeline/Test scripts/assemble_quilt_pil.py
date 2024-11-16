import os
from math import ceil
from PIL import Image
from PIL import ImageShow
import glob

frames = []
width = 0
height = 0
for filename in glob.glob('GreenBuddha/*'):
    im = Image.open(filename)
    frames.append(im)
    width, height = im.size
    print(f"{filename} {im.size}")

rows = 5
columns = ceil(len(frames)/rows)
print(f"{width}x{height} {rows} rows, {columns} columns")
quilt = Image.new('RGB', (width*columns, height*rows))
print(quilt.size)

i = 0
for y in reversed(range(0, height*rows, height)):
    for x in range(0, width*columns, width):
        if i<len(frames):
            quilt.paste(frames[i], (x, y))
        i += 1

newTargetDir = filename = "GreenBuddha"
quiltPath = f"{newTargetDir}/{filename}_qs{columns}x{rows}a{9 / 16}.jpg"

print(quiltPath)
if os.path.isfile(quiltPath):
    os.remove(quiltPath)
quilt.save(quiltPath)
ImageShow.show(quilt)


