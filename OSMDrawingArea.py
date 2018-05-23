import math
import requests
from PIL import Image
import gi
import cairo
import numpy
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class OSMDrawingArea(Gtk.DrawingArea):
    def __init__(self, resolution=[640, 480]):
        Gtk.DrawingArea.__init__(self)
        self.resolution = resolution    # начальное разрешение

        self.connect("draw", self.doDraw)   # привязка отрисовки
        self.connect("unrealize", self.doUnrealize)  # привязка освобождения ресурсов
        self.set_size_request(resolution[0], resolution[1])     # ставим начальное разрешение на виджет

        self.tileSizeX = 256     # размер тайлов в пикселях
        self.tileSizeY = 256

        self.tileMap = []   # массив отображаемых тайлов

        self.upperBoundLat = 90  # Верхняя граница широты отображаемой карты
        self.bottomBoundLat = -90     # Нижняя граница широты
        self.leftBoundLon = 0   # левая граница долготы
        self.rightBoundLon = 180      # правая граница долготы

        self.centerLon = 37.612    # координаты центра карты
        self.centerLat = 55.743   #

        self.zoom = 18

    def doDraw(self, widget, cr):   # рендеринг
        widgetAlloc = self.get_allocation()     # получаем разрешение виджета
        image = Image.new("RGB", (widgetAlloc.width, widgetAlloc.height))
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

    def doUnrealize(self, arg):     # освобождение ресурсов
        pass

    def lon2tilex(self, lon, zoom):     # долготу в координату тайла
        return int((lon + 180) / 360 * 2 ** zoom)

    def lat2tiley(self, lat, zoom):     # широту в координату тайла
        lat = lat * math.pi / 180
        return int((1 - math.log(math.tan(lat) + 1 / math.cos(lat)) / math.pi) / 2 * 2 ** zoom)

    def tile2path(self, tilex, tiley, zoom):    # координаты тайла в путь
        return "http://tile.openstreetmap.org/%d/%d/%d.png" % (zoom, tilex, tiley)


