# -*- coding: utf-8 -*-
from gettext import gettext as _
import logging
from IconRequests.const import DESKTOP_FILE_DIRS, settings, repositories, ICONS_IGNORE_LIST
from IconRequests.utils import (get_supported_icons, is_gnome,
                                is_app_menu, get_issues_list)
from IconRequests.modules.upload.imgur import Imgur
from IconRequests.modules.desktop import DesktopFile
from IconRequests.widgets.notification import Notification
from IconRequests.widgets.application_row import ApplicationRow
from threading import Thread
from os import path
from glob import glob
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GObject, GLib



class Window(Gtk.ApplicationWindow, GObject.GObject):
    __gsignals__ = {
        'loaded': (GObject.SIGNAL_RUN_FIRST, None, (bool,))
    }

    def __init__(self, application):
        GObject.GObject.__init__(self)
        # Initiate the uploading server
        self.upload_service = Imgur(settings)
        self.builder = Gtk.Builder.new_from_resource(
            "/org/gnome/IconRequests/ui/mainwindow.ui")
        self.generate_window(application)

    def generate_window(self, application):
        self.window = self.builder.get_object("MainWindow")
        self.window.connect("key-press-event", self.__on_key_press)

        notification = self.builder.get_object("Notification")
        notification_msg = self.builder.get_object("NotificationMessage")

        self.notification = Notification(notification, notification_msg)

        position_x, position_y = settings.get_window_position()
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

        self.menu_button = self.builder.get_object("PopoverMenuButton")
        if not is_gnome() or is_app_menu():
            self.menu_button.set_visible(True)
            self.popover = Gtk.Popover.new_from_model(self.menu_button, application.menu)
            self.popover.props.width_request = 200
            self.menu_button.connect("clicked", self.show_menu_popover)

        self.revealer = self.builder.get_object("Revealer")
        self.search_list = [self.all, self.unsupported, self.hardcoded]

        self.main_stack.set_visible_child_name("loading")
        # Watch the icon name gsettings
        self.gsettings = Gio.Settings.new("org.gnome.desktop.interface")
        self.gsettings.connect("changed", self.refresh_icons_view)

        self.start()

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def refresh_icons_view(self, gsettings, key):
        if key == "icon-theme":
            self.main_stack.set_visible_child_name("loading")
            for listbox in self.search_list:
                for child in listbox.get_children():
                    listbox.remove(child)
            self.search_button.set_active(False)
            self.search_entry.set_text("")
            self.start()

    def start(self):
        thread = Thread(target=self.generate_apps_list)
        thread.daemon = True
        thread.start()

    def __on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval).lower()
        if keyname == 'escape' and self.search_button.get_active():
            if self.search_entry.is_focus():
                self.search_button.set_active(False)
                self.search_entry.set_text("")
            else:
                self.search_entry.grab_focus_without_selecting()
            return True

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
            self.main_stack.set_visible_child_name("applications")
        else:
            self.revealer.set_reveal_child(True)
            self.search_entry.grab_focus_without_selecting()

    def filter_func(self, row, data, notify_destroy):
        """
            Filter function, used to check if the entered data exists on the application ListBox
        """
        app_label = row.desktop_file.getName()
        data = data.lower()
        if len(data) > 0:
            return data in app_label.lower()
        else:
            self.main_stack.set_visible_child_name("applications")
            return True

    def __filter_applications(self, entry):
        data = entry.get_text().strip()
        for search_list in self.search_list:
            stack = search_list.get_parent().get_parent().get_parent()
            search_list.set_filter_func(self.filter_func, data, True)

    def show_menu_popover(self, *args):
        if self.popover:
            if self.popover.get_visible():
                self.popover.hide()
            else:
                self.popover.show_all()

    def show_window(self):
        self.window.show_all()
        self.window.present()

    def generate_apps_list(self):
        self.builder.get_object("loadingSpinner").start()
        supported_icons = get_supported_icons()
        theme = Gio.Settings.new("org.gnome.desktop.interface").get_string("icon-theme")
        repo = None
        try:
            repo = repositories.get_repo(theme)
        except KeyError:
            pass
        issues_list = []
        if repo:
            issues_list = get_issues_list(repo)
        self.db = []
        already_added = []
        for desktop_dir in DESKTOP_FILE_DIRS:
            if path.isdir(desktop_dir):
                all_files = glob("{0}*.desktop".format(desktop_dir))
                for desktop_file in all_files:
                    obj = DesktopFile(desktop_file, self.upload_service,
                                      supported_icons, issues_list)
                    icon_name = obj.getIcon()
                    if icon_name not in already_added and icon_name not in ICONS_IGNORE_LIST:
                        self.db.append(obj)
                        already_added.append(icon_name)
        self.db = sorted(self.db, key=lambda x: x.getName().lower())
        self.emit("loaded", True)
        return False

    def do_loaded(self, signal):
        if signal:
            for desktop_file in self.db:
                row = ApplicationRow(desktop_file, self.notification)
                if desktop_file.is_hardcoded:
                    self.hardcoded.add(row)
                elif not desktop_file.is_supported:
                    self.unsupported.add(row)
                else:
                    self.all.add(row)
            self.builder.get_object("loadingSpinner").stop()
            self.main_stack.set_visible_child_name("applications")
            self.all.show_all()
            self.hardcoded.show_all()
            self.unsupported.show_all()

    def save_window_state(self):
        settings.set_window_postion(self.window.get_position())
