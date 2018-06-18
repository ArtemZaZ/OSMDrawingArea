import gi
gi.require_version("Gtk", "3.0")
import OSMDrawingArea
from gi.repository import Gtk


def draw(self, widget, cr, screenLL):
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(3)
    cr.move_to(0, 0)
    cr.line_to(100, 100)
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
