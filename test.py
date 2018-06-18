from PIL import Image
import math
import requests
import urllib


def tilex2lon(tilex, zoom):
    return 360 * tilex / (2 ** zoom) - 180


def tiley2lat(tiley, zoom):
    return math.atan(math.sinh(math.pi * (1 - 2 * tiley / (2 ** zoom)))) * 180 / math.pi


def lon2tilex(lon, zoom):
    return ((lon + 180) / 360 * 2 ** zoom)


def lat2tiley(lat, zoom):
    lat = lat*math.pi/180
    return ((1 - math.log(math.tan(lat) + 1/math.cos(lat))/math.pi) / 2 * 2 ** zoom)


def tile2path(tilex, tiley, zoom):
    return "http://tile.openstreetmap.org/%d/%d/%d.png" % (zoom, tilex, tiley)


im = Image.new("RGB", (1622, 1000))
img = Image.open("ring.png")
img1 = Image.open("kompas.png")

im.paste(img, (-200, 0))
im.paste(img1, (722, 0))
#im.show()

zoom = 18

tilex = lon2tilex(30.52060, zoom)
tiley = lat2tiley(59.91541, zoom)


path = tile2path(tilex, tiley, zoom)
path2 = tile2path(tilex+1, tiley, zoom)

print(path)
response = requests.get(path, stream=True)
tile = Image.open(response.raw)
response = requests.get(path2, stream=True)
tile2 = Image.open(response.raw)
tilemap = Image.new("RGB", (256, 256))
tilemap.paste(tile, (0, 0))
#tilemap.paste(tile2, (256, 0))
tilemap.show()

lontemp = tilex2lon(tilex, zoom)
lattemp = tiley2lat(tiley, zoom)

print(lontemp)
print(lattemp)



