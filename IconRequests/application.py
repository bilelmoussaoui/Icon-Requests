#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio, Gdk, GObject
from IconRequests.widgets.window import Window
from IconRequests.utils import is_gnome
from gettext import gettext as _
import logging
import signal


class Application(Gtk.Application):
    win_object = None
    alive = True

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.IconRequests",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(_("Icon Requests"))
        GLib.set_prgname("Icon Requests")

        self.menu = Gio.Menu()
        cssProviderFile = Gio.File.new_for_uri(
            'resource:///org/gnome/IconRequests/style.css')
        cssProvider = Gtk.CssProvider()
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        try:
            cssProvider.load_from_file(cssProviderFile)
            styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
            logging.debug("Loading css file ")
        except Exception as e:
            logging.error("Error message %s" % str(e))

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.generate_menu()

    def generate_menu(self):
        # Help section
        help_content = Gio.Menu.new()
        if Gtk.get_major_version() >= 3 and Gtk.get_minor_version() >= 20:
            help_content.append_item(Gio.MenuItem.new(
                _("Shortcuts"), "app.shortcuts"))

        help_content.append_item(Gio.MenuItem.new(_("About"), "app.about"))
        help_content.append_item(Gio.MenuItem.new(_("Quit"), "app.quit"))
        help_section = Gio.MenuItem.new_section(None, help_content)
        self.menu.append_item(help_section)

        if Gtk.get_major_version() >= 3 and Gtk.get_minor_version() >= 20:
            action = Gio.SimpleAction.new("shortcuts", None)
            action.connect("activate", self.on_shortcuts)
            self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        if is_gnome():
            self.set_app_menu(self.menu)
            logging.debug("Adding gnome shell menu")

    def do_activate(self, *args):
        if not self.win_object:
            self.win_object = Window(self)
            self.win_object.show_window()
            self.win = self.win_object.window
            self.add_window(self.win)
        else:
            self.win_object.show_window()

    def on_shortcuts(self, *args):
        """
            Shows keyboard shortcuts
        """
        shortcuts = Application.shortcuts_dialog()
        if shortcuts:
            shortcuts.set_transient_for(self.win)
            shortcuts.show()

    @staticmethod
    def shortcuts_dialog():
        if Gtk.get_major_version() >= 3 and Gtk.get_minor_version() >= 20:
            builder = Gtk.Builder()
            builder.add_from_resource('/org/gnome/IconRequests/shortcuts.ui')
            shortcuts = builder.get_object("shortcuts")
            return shortcuts
        return None

    @staticmethod
    def about_dialog():
        """
            Shows about dialog
        """
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gnome/IconRequests/about.ui')

        dialog = builder.get_object("AboutDialog")
        return dialog

    def on_about(self, *args):
        """
            Shows about dialog
        """
        dialog = Application.about_dialog()
        dialog.set_transient_for(self.win)
        dialog.run()
        dialog.destroy()

    def on_quit(self, *args):
        """
        Close the application, stops all threads
        and clear clipboard for safety reasons
        """
        self.alive = False
        signal.signal(signal.SIGINT, lambda x, y: self.alive)
        if self.win:
            self.win_object.save_window_state()
            self.win.destroy()
        self.quit()
