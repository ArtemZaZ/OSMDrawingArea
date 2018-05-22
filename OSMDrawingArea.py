import math
import requests
from PIL import Image
import gi
gi.require_version("Gtk", "3.0")


class OSMDrawingArea(Gtk.DrawingArea):
    def __init__(self, resolution = [640, 480]):
        Gtk.DrawingArea.__init__(self)
        self.resolution = resolution    # начальное разрешение

        self.connect("draw", self.doDraw)   # привязка отрисовки
        self.connect("unrealize", self.doUnrealize)  # привязка освобождения ресурсов
        self.set_size_request(resolution[0], resolution[1])     # ставим начальное разрешение на виджет

    def doDraw(self, widget, cr):
        pass

    def doUnrealize(self, arg):
        pass


