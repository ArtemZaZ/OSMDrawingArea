from PIL import Image
import math
import requests
import urllib


def lon2tilex(lon, zoom):
    return int((lon + 180) / 360 * 2 ** zoom)


def lat2tiley(lat, zoom):
    lat = lat*math.pi/180
    return int((1 - math.log(math.tan(lat) + 1/math.cos(lat))/math.pi) / 2 * 2 ** zoom)


def tile2path(tilex, tiley, zoom):
    return "http://tile.openstreetmap.org/%d/%d/%d.png" % (zoom, tilex, tiley)


im = Image.new("RGB", (1622, 1000))
img = Image.open("ring.png")
img1 = Image.open("kompas.png")

im.paste(img, (0, 0))
im.paste(img1, (722, 0))
#im.show()

tilex = lon2tilex(-1.225, 7)
tiley = lat2tiley(51.744, 7)
path = tile2path(tilex, tiley, 7)

response = requests.get(path, stream=True)
tile = Image.open(response.raw)
print(tile.height)
tile.show()
