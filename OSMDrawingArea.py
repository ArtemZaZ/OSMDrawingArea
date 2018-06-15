import math
import requests
from PIL import Image
import gi
import cairo
import numpy
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

"""
tile and lon/lat convertation: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
"""


class OSMDrawingArea(Gtk.DrawingArea):
    def __init__(self, resolution=[640, 480]):
        Gtk.DrawingArea.__init__(self)
        self.resolution = resolution    # начальное разрешение

        self.connect("draw", self.render)   # привязка отрисовки
        self.connect("unrealize", self.doUnrealize)  # привязка освобождения ресурсов
        self.set_size_request(resolution[0], resolution[1])     # ставим начальное разрешение на виджет

        self.tileSize = [256, 256]
        self.tileMap = []   # массив отображаемых тайлов
        self.screenLL = [0, 0, 0, 0]  # параметры экрана в lon и lat
        self.center = [37.612, 37.612]  # координаты центра экрана
        self.zoom = 18

    def render(self, widget, cr):   # рендеринг
        widgetAllocation = self.get_allocation()     # получаем разрешение виджета
        image = Image.new("RGB", (widgetAllocation.width, widgetAllocation.height))     # создаем изображение на
        # котором будем все склеивать
        tilex = self.lon2tilex(self.center[0], self.zoom)
        tiley = self.lat2tiley(self.center[1], self.zoom)
        startDrawingCoords = [widgetAllocation.width / 2 - (tilex - int(tilex)) * self.tileSize[0], widgetAllocation.height / 2 - (tiley - int(tiley)) * self.tileSize[1]]
        # получаем координаты первого(центрального) тайла для отрисовки в пикселях
        scope = self.delimitation(widgetAllocation, startDrawingCoords, self.tileSize)
        # определяем параметры экрана в широте и долготе
        self.screenLL[0] = self.tilex2lon(int(tilex) - int(scope[0]) + scope[0] % 1, self.zoom)     # координаты
        self.screenLL[1] = self.tiley2lat(int(tiley) - int(scope[2]) + scope[2] % 1, self.zoom)
        self.screenLL[2] = self.tilex2lon(int(tilex) + int(scope[1]) + scope[1] % 1, self.zoom) - self.screenLL[0]  #
        #  ширина и высота
        self.screenLL[3] = self.tiley2lat(int(tiley) + int(scope[3]) + scope[3] % 1, self.zoom) - self.screenLL[1]

        tempTilex = tilex - math.ceil(scope[0])
        tempTiley = tiley - math.ceil(scope[2])
        startDrawingCoords = [startDrawingCoords[0] - math.ceil(scope[0]) * self.tileSize[0], startDrawingCoords[1] - math.ceil(scope[2]) * self.tileSize[1]]

        for i in range(math.ceil(scope[1]) + math.ceil(scope[3])):
            for j in range(math.ceil(scope[0]) + math.ceil(scope[2])):
                path = self.tile2path(tempTilex + i, tempTiley + j, self.zoom)
                print(path)
                response = requests.get(path, stream=True)
                tile = Image.open(response.raw)
                image.paste(tile, (int(startDrawingCoords[0] + i * self.tileSize[0]), int(startDrawingCoords[1] + j * self.tileSize[1])))
        image.putalpha(255)
        arr = numpy.array(image)
        surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, widgetAllocation.width, widgetAllocation.height)
        pt = cairo.SurfacePattern(surface)
        pt.set_extend(cairo.EXTEND_REPEAT)
        cr.set_source(pt)
        cr.rectangle(0, 0, widgetAllocation.width, widgetAllocation.height)
        cr.fill()



        """
        widgetAlloc = self.get_allocation()     # получаем разрешение виджета
        
        tempWidth = widgetAlloc.width
        tempHeight = widgetAlloc.height
        temp = tempWidth
        tilex = self.lon2tilex(self.centerLon, self.zoom)
        tiley = self.lat2tiley(self.centerLat, self.zoom)
        i = 0
        j = 0
        while tempHeight > 0:
            tempWidth = temp
            i = 0
            while tempWidth > 0:
                path = self.tile2path(tilex + i, tiley + j, self.zoom)
                print(path)
                response = requests.get(path, stream=True)
                tile = Image.open(response.raw)
                image.paste(tile, (i*self.tileSizeX, j*self.tileSizeY))
                tempWidth -= self.tileSizeX
                print(i)
                i = i + 1
            j = j + 1
            tempHeight -= self.tileSizeY
        image.putalpha(255)
        arr = numpy.array(image)
        surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, widgetAlloc.width, widgetAlloc.height)
        pt = cairo.SurfacePattern(surface)
        pt.set_extend(cairo.EXTEND_REPEAT)
        cr.set_source(pt)
        cr.rectangle(0, 0, widgetAlloc.width, widgetAlloc.height)
        cr.fill()
        """

    def doUnrealize(self, arg):     # освобождение ресурсов
        pass

    def delimitation(self, wa, sd, ts):     # определение границ отрисовываемой карты в тайлах по размерам экрана,
        # начальной координате и размеру тайла
        leftBorder = sd[0] / ts[0]
        rightBorder = (wa.width - sd[0]) / ts[0]
        upperBorder = sd[1] / ts[1]
        downBorder = (wa.height - sd[1]) / ts[1]
        return [leftBorder, rightBorder, upperBorder, downBorder]

    def lon2tilex(self, lon, zoom):     # долготу в координату тайла
        return (lon + 180) / 360 * 2 ** zoom

    def lat2tiley(self, lat, zoom):     # широту в координату тайла
        lat = lat * math.pi / 180
        return (1 - math.log(math.tan(lat) + 1 / math.cos(lat)) / math.pi) / 2 * 2 ** zoom

    def tilex2lon(self, tilex, zoom):
        return 360 * tilex / (2 ** zoom) - 180

    def tiley2lat(self, tiley, zoom):
        return math.atan(math.sinh(math.pi * (1 - 2 * tiley / (2 ** zoom)))) * 180 / math.pi

    def tile2path(self, tilex, tiley, zoom):    # координаты тайла в путь
        return "http://tile.openstreetmap.org/%d/%d/%d.png" % (zoom, tilex, tiley)


