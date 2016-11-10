# -*- coding: utf-8 -*-

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GObject, GLib
from gettext import gettext as _
from widgets.headerbar import HeaderBar
import logging
from widgets.applications_list import ApplicationsList
from widgets.search_bar import SearchBar

class Window(Gtk.ApplicationWindow):
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

    def __init__(self, application):
        self.app = application
        self.generate_window()
        self.generate_headerbar()
        self.generate_components()

    def generate_window(self, *args):
        """
            Generate application window (Gtk.Window)
        """
        Gtk.ApplicationWindow.__init__(self, type=Gtk.WindowType.TOPLEVEL,
                                       application=self.app)
        self.set_wmclass("Numix Icon Reporter", "numix-icon-report")
        self.set_icon_name("numix-icon-report")
        self.resize(400, 650)
        self.set_size_request(400, 650)
        self.set_resizable(True)
        self.connect("delete-event", lambda x, y: self.app.on_quit())
        self.add(self.main_box)


    def generate_headerbar(self):
        self.hb = HeaderBar(self)
        self.set_titlebar(self.hb)

    def generate_components(self):

        self.all_box = Gtk.ScrolledWindow()

        all_list = ApplicationsList(self, "all")
        self.all_box.add(all_list)
        self.hb.stack.add_titled(self.all_box, "all", _("All"))

        self.unsupported_box = Gtk.ScrolledWindow()
        unsupported_list = ApplicationsList(self, "unsupported")
        self.unsupported_box.add(unsupported_list)
        self.hb.stack.add_titled(self.unsupported_box, "unsupported", _("Unsupported"))

        self.hardcoded_box = Gtk.ScrolledWindow()
        hardcoded_list = ApplicationsList(self, "hardcoded")
        self.hardcoded_box.add(hardcoded_list)
        self.hb.stack.add_titled(self.hardcoded_box, "hardcoded", _("Hardcoded"))
        self.search_bar = SearchBar(all_list, unsupported_list, hardcoded_list, self,
                            self.hb.search_button)
        self.main_box.add(self.search_bar)
        self.main_box.add(self.hb.stack)
