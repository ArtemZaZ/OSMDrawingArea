import gi
gi.require_version("Gtk", "3.0")
import OSMDrawingArea
from gi.repository import Gtk
import LogParser


def draw(self, widget, cr, screenLL):
    allocation = self.get_allocation()
    self.setCenter(30.342022, 59.864629)
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(2)
    print(screenLL)
    print(screenLL[0] - LogParser.LatLon[0][1], screenLL[1] - LogParser.LatLon[0][0])
    print((screenLL[0] - LogParser.LatLon[0][1])/screenLL[2], (screenLL[1] - LogParser.LatLon[0][0])/screenLL[3])
    cr.move_to(int(allocation.width*(screenLL[0] - LogParser.LatLon[0][1])/screenLL[2]), int(allocation.height*(screenLL[1] - LogParser.LatLon[0][0])/screenLL[3]))
    for i in LogParser.LatLon[1:]:
        print(i[1], i[0])
        cr.line_to(int(allocation.width*(screenLL[0] - i[1])/screenLL[2]), int(allocation.height*(screenLL[1] - i[0])/screenLL[3]))
        cr.stroke()
    print(111)


class Pult:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("test.glade")
        self.window = self.builder.get_object("window1")
        self.button = self.builder.get_object("button1")
        self.box = self.builder.get_object("box2")  # бокс под виджет
        self.window.connect("delete-event", self.delete_event)

        self.OSMDA = OSMDrawingArea.OSMDrawingArea(resolution=[640, 480], drawcallback=draw)  # виджет
        self.box.pack_start(self.OSMDA, True, True, 0)
        self.window.show_all()
        Gtk.main()

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()


p = Pult()
