#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gettext import gettext as _


from .modules import Logger, Settings

from .utils import is_app_menu, is_gnome
from .widgets import AboutDialog, Window

from gi import require_version
require_version("Gtk", "3.0")
require_version("Gdk", "3.0")
from gi.repository import Gdk, Gio, GLib, Gtk




class Application(Gtk.Application):
    ALIVE = True

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="com.github.bilelmoussaoui.IconRequests",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(_("Icon Requests"))
        GLib.set_prgname("Icon Requests")

        self._load_css()
        gtk_settings = Gtk.Settings.get_default()
        gtk_settings.props.gtk_application_prefer_dark_theme = Settings.get_default().night_mode
        self._menu = Gio.Menu()

    def _load_css(self):
        css_file = 'resource:///com/github/bilelmoussaoui/IconRequests/css/style.css'
        css_provider_file = Gio.File.new_for_uri(css_file)
        css_provider = Gtk.CssProvider()
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        try:
            css_provider.load_from_file(css_provider_file)
            style_context.add_provider_for_screen(screen, css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_USER)
        except GLib.Error as error:
            Logger.error(error)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self._generate_menu()
        self._generate_actions()
        if is_gnome() and not is_app_menu():
            self.set_app_menu(self._menu)

    @property
    def menu(self):
        return self._menu

    def _generate_menu(self):
        # Help section
        help_content = Gio.Menu.new()
        help_content.append_item(Gio.MenuItem.new(_("Night Mode"),
                                                  "app.night_mode"))
        help_content.append_item(Gio.MenuItem.new(_("About"),
                                                  "app.about"))
        help_content.append_item(Gio.MenuItem.new(_("Quit"),
                                                  "app.quit"))
        help_section = Gio.MenuItem.new_section(None, help_content)
        self._menu.append_item(help_section)

    def _generate_actions(self):
        night_mode = GLib.Variant.new_boolean(
            Settings.get_default().night_mode)
        action = Gio.SimpleAction.new_stateful("night_mode", None, night_mode)
        action.connect("change-state", self._on_night_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self._on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self._on_quit)
        self.add_action(action)

    def do_activate(self, *args):
        window = Window.get_default()
        window.set_application(self)
        self.add_window(window)
        window.show_all()

    def _on_night_mode(self, action, gvariant):
        settings = Settings.get_default()
        is_night_mode = not settings.night_mode
        action.set_state(GLib.Variant.new_boolean(is_night_mode))
        settings.night_mode = is_night_mode
        Gtk.Settings.get_default().set_property(
            "gtk-application-prefer-dark-theme",
            is_night_mode
        )

    def _on_about(self, *args):
        """
            Shows about dialog
        """
        dialog = AboutDialog()
        dialog.set_transient_for(Window.get_default())
        dialog.run()
        dialog.destroy()

    def _on_quit(self, *args):
        """
        Close the application, stops all threads
        and clear clipboard for safety reasons
        """
        ALIVE = False
        window = Window.get_default()
        if window:
            window.close()
        self.quit()
