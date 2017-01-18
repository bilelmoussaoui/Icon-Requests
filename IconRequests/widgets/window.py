# -*- coding: utf-8 -*-

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GObject, GLib
from gettext import gettext as _
import logging
from IconRequests.const import DESKTOP_FILE_DIRS
from IconRequests.modules.settings import Settings
from IconRequests.modules.desktop import DesktopFile, DesktopFileCorrupted, DesktopFileInvalid
from IconRequests.widgets.headerbar import HeaderBar
from IconRequests.widgets.search_bar import SearchBar
from IconRequests.widgets.application_row import ApplicationRow
from threading import Thread
from os import path, listdir


class Window(Gtk.ApplicationWindow, Thread, GObject.GObject):
    __gsignals__ = {
        'loaded': (GObject.SIGNAL_RUN_FIRST, None, (bool,))
    }
    db = []

    def __init__(self, application):
        GObject.GObject.__init__(self)
        Thread.__init__(self)
        self.settings = Settings.new()

        self.builder = Gtk.Builder.new_from_resource(
            "/org/gnome/IconRequests/mainwindow.ui")
        self.window = self.builder.get_object("MainWindow")
        self.window.connect("key-press-event", self.__on_key_press)

        position_x, position_y = self.settings.get_window_position()
        if position_x and position_y:
            self.window.move(position_x, position_y)
        else:
            self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.stack = self.builder.get_object("Stack")
        self.main_stack = self.builder.get_object("MainStack")
        # Listbox
        self.all = self.builder.get_object("AllListBox")
        self.unsupported = self.builder.get_object("unsupportedListBox")
        self.hardcoded = self.builder.get_object("hardcodedListBox")
        self.window.set_application(application)
        self.window.connect("delete-event", lambda x, y: application.on_quit())

        self.search_button = self.builder.get_object("SearchButton")
        self.search_button.connect("toggled", self.__toggle_search)

        self.search_entry = self.builder.get_object("searchEntry")
        self.search_entry.set_width_chars(28)
        self.search_entry.connect("search-changed", self.__filter_applications)

        self.revealer = self.builder.get_object("Revealer")
        self.search_list = [self.all, self.unsupported, self.hardcoded]

        self.main_stack.set_visible_child_name("loading")
        self.start()

    def __on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval).lower()
        if keyname == 'escape' and self.search_button.get_active():
            if self.search_entry.is_focus():
                self.search_button.set_active(False)
                self.search_entry.set_text("")
            else:
                self.search_entry.grab_focus_without_selecting()

        if keyname == "backspace":
            if (len(self.search_entry.get_text()) == 0
                    and self.revealer.get_reveal_child()):
                self.search_button.set_active(False)
                return True

        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if keyname == 'f':
                self.search_button.set_active(
                    not self.search_button.get_active())
                return True
        return False

    def __toggle_search(self, *args):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            self.search_entry.set_text("")
            for search_list in self.search_list:
                search_list.set_filter_func(lambda x, y, z: True, None, False)
        else:
            self.revealer.set_reveal_child(True)
            self.search_entry.grab_focus_without_selecting()

    def filter_func(self, row, data, notify_destroy):
        """
            Filter function, used to check if the entered data exists on the application ListBox
        """
        app_label = row.get_name()
        data = data.lower()
        if len(data) > 0:
            return data in app_label.lower()
        else:
            return True

    def __filter_applications(self, entry):
        data = entry.get_text().strip()
        for search_list in self.search_list:
            search_list.set_filter_func(self.filter_func, data, False)

    def show_window(self):
        self.window.show_all()
        self.window.present()

    def run(self):
        self.builder.get_object("loadingSpinner").start()
        already_added = []
        for desktop_dir in DESKTOP_FILE_DIRS:
            if path.isdir(desktop_dir):
                all_files = listdir(desktop_dir)
                for desktop_file in all_files:
                    desktop_file_path = desktop_dir + desktop_file
                    ext = path.splitext(desktop_file)[1].lower().strip(".")
                    if ext == "desktop" and desktop_file not in already_added:
                        try:
                            self.db.append(DesktopFile(desktop_file_path))
                            already_added.append(desktop_file)
                        except DesktopFileCorrupted:
                            logging.error(
                                "Desktop file corrupted {0}".format(desktop_file))
                        except DesktopFileInvalid:
                            logging.debug(
                                "Desktop file not displayed {0}".format(desktop_file))
        self.db = sorted(self.db, key=lambda x: x.name.lower())
        self.emit("loaded", True)

    def do_loaded(self, signal):
        if signal:
            for desktop_file in self.db:
                if desktop_file.is_hardcoded:
                    self.hardcoded.add(ApplicationRow(desktop_file))
                if not desktop_file.is_supported:
                    self.unsupported.add(ApplicationRow(desktop_file))
                self.all.add(ApplicationRow(desktop_file))

            self.main_stack.set_visible_child_name("applications")
            self.all.show_all()
            self.hardcoded.show_all()
            self.unsupported.show_all()
            self.builder.get_object("loadingSpinner").stop()

    def save_window_state(self):
        self.settings.set_window_postion(self.window.get_position())
