#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi import require_version
require_version("Gtk", "3.0")
require_version("GnomeKeyring", "1.0")
from gi.repository import Gtk, GLib, Gio, Gdk, GObject
from widgets.window import Window
from utils import is_gnome
from gettext import gettext as _
import logging
import signal


class Application(Gtk.Application):
    win = None
    alive = True
    send_sms_action = None
    send_sms_window = None

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.Icon.Report",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(_("Numix Icon Reporter"))
        GLib.set_prgname("Numix Icon Reporter")

        self.menu = Gio.Menu()

        cssProviderFile = "./data/style.css"
        cssProvider = Gtk.CssProvider()
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        try:
            cssProvider.load_from_path(cssProviderFile)
            styleContext.add_provider_for_screen(screen, cssProvider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_USER)
            logging.debug("Loading css file ")
        except Exception as e:
            logging.error("Error message %s" % str(e))

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.generate_menu()

    def generate_menu(self):
        # Settings section
        settings_content = Gio.Menu.new()
        settings_content.append_item(
            Gio.MenuItem.new(_("Settings"), "app.settings"))
        settings_section = Gio.MenuItem.new_section(None, settings_content)
        self.menu.append_item(settings_section)

        # Help section
        help_content = Gio.Menu.new()
        if Gtk.get_major_version() >= 3 and Gtk.get_minor_version() >= 20:
            help_content.append_item(Gio.MenuItem.new(
                _("Shortcuts"), "app.shortcuts"))

        help_content.append_item(Gio.MenuItem.new(_("About"), "app.about"))
        help_content.append_item(Gio.MenuItem.new(_("Quit"), "app.quit"))
        help_section = Gio.MenuItem.new_section(None, help_content)
        self.menu.append_item(help_section)

        self.send_sms_action = Gio.SimpleAction.new("send_sms", None)
        self.send_sms_action.connect("activate", self.on_send_sms)
        self.add_action(self.send_sms_action)

        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.on_settings)
        self.add_action(settings_action)

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
        if not self.win:
            self.win = Window(self)
            self.win.show_all()
            self.add_window(self.win)
        else:
            self.win.present()

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
            builder.add_from_resource('/org/gnome/TwoFactorAuth/shortcuts.ui')
            shortcuts = builder.get_object("shortcuts")
            return shortcuts
        return None

    @staticmethod
    def about_dialog():
        """
            Shows about dialog
        """
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gnome/TwoFactorAuth/about.ui')

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

    def on_settings(self, *args):
        """
            Shows settings window
        """
        pass

    def on_send_sms(self, *args):
        """
            Show SMS window
        """
        print(self.send_sms_window)
        if self.send_sms_window is not None:
            self.send_sms_window.present()
        else:
            self.send_sms_window = SendSMSWindow(self.win)
        self.send_sms_window.show_window()

    def on_quit(self, *args):
        """
        Close the application, stops all threads
        and clear clipboard for safety reasons
        """
        self.alive = False
        signal.signal(signal.SIGINT, lambda x, y: self.alive)
        if self.win:
            # self.win.save_window_state()
            self.win.destroy()
        self.quit()
