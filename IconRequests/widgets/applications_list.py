from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gio, GLib, Gdk
from gettext import gettext as _
import logging
from IconRequests.widgets.application_row import ApplicationRow
import sys
sys.path.insert(0, '../')
from IconRequests.utils import get_desktop_files_info


class ApplicationsList(Gtk.ListBox):

    def __init__(self, parent, type):
        self.parent = parent
        self.type = type
        Gtk.ListBox.__init__(self)
        self.get_style_context().add_class("applications-list")
        self.generate()

    def generate(self):
        desktop_files = get_desktop_files_info()
        sorted(desktop_files, key=lambda x: desktop_files[x]["name"])
        if len(desktop_files) != 0:
            for desktop_file in desktop_files:
                desktop_info = desktop_files[desktop_file]
                if self.type == "hardcoded":
                    if desktop_info["is_hardcoded"]:
                        self.add(ApplicationRow(desktop_info, self))
                elif self.type == "unsupported":
                    if not desktop_info["is_supported"]:
                        self.add(ApplicationRow(desktop_info, self))
                else:
                    self.add(ApplicationRow(desktop_info, self))
        else:
            print("nothing to show")

    def refresh(self):
        self.generate()
        self.show_all()

    def append(self, application):
        self.add(ApplicationRow(application, self))
        self.show_all()
