# -*- coding: utf-8 -*-
from gettext import gettext as _

from os import path
from glob import glob
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk

from IconRequests.const import App
from IconRequests.controller.applications import ApplicationsController
from IconRequests.modules.settings import Settings
from IconRequests.utils import is_gnome, is_app_menu
from IconRequests.widgets.headerbar import HeaderBar
from IconRequests.widgets.loading import Loading
from IconRequests.widgets.notification import Notification
from IconRequests.widgets.search_bar import SearchBar
from IconRequests.widgets.applications.list import ApplicationsList


class Window(Gtk.ApplicationWindow):
    _instance = None

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self,
                                       type=Gtk.WindowType.TOPLEVEL)
        # Window configuration
        self.set_resizable(False)
        self.set_default_size(400, 600)
        self.set_size_request(400, 600)
        self._restore_state()
        self.set_wmclass("icon-requests", "Icon Requests")
        self.set_icon_name("icon-requests")
        self.set_titlebar(HeaderBar.get_default())
        self.connect("delete-event", self.close)
        # Widgets creation
        self._build_widgets()

    @staticmethod
    def get_default():
        """Return default instance of Window."""
        if Window._instance is None:
            Window._instance = Window()
        return Window._instance

    def _build_widgets(self):
        # Main Container: SearchBar, Notification, Loading & Stack
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        headerbar = HeaderBar.get_default()
        # Notification
        self._notification = Notification()
        # Stack
        self._stack = Gtk.Stack()
        self._all = ApplicationsList()
        self._unsupported = ApplicationsList()
        # For StackSwitcher
        headerbar.set_stack(self._stack)
        # Loading Container
        self._loading = Loading()
        self._loading.start()
        # SearchBar
        self._search_bar = SearchBar()
        self._search_bar.connect_button(headerbar.search_button)
        self._search_bar.add_data_source([self._all.listbox,
                                          self._unsupported.listbox
                                         ])

        container.pack_start(self._search_bar, False, False, 0)
        container.pack_start(self._notification, False, False, 0)
        container.pack_start(self._loading, True, True, 0)
        container.pack_start(self._stack, True, True, 0)
        # Hide Stack by default (shows loading window)
        self._stack.set_visible(False)
        self._stack.set_no_show_all(True)
        # Application Menu Popover
        if not is_gnome() or is_app_menu():
            menu_button = headerbar.menu_button
            menu_button.show()
            popover = Gtk.Popover.new_from_model(menu_button, App().menu)
            menu_button.connect("clicked", self._toggle_popover, popover)
        self.add(container)
        self._load_applications()


    """TODO:
    - Refactor this fucking function
    """
    def _load_applications(self):

        controller = ApplicationsController()

        def set_loading(app_name):
            self._loading.label = app_name
        controller.connect("parse", lambda event, app_name: set_loading(app_name))

        def fill_aplications_list(controller):
            for app in controller.database:
                if app.is_hardcoded or not app.is_supported:
                    self._unsupported.append(app)
                else:
                    self._all.append(app)
            self._stack.add_titled(self._all, "all",
                                   _("All"))
            self._stack.add_titled(self._unsupported, "unsupported",
                                   _("Unsupported"))
            self._loading.stop()
            self._loading.set_visible(False)
            self._stack.set_visible(True)

        controller.connect("loaded", fill_aplications_list)

    def _toggle_popover(self, button, popover):
        """Toggle Menu popover."""
        if popover:
            if popover.get_visible():
                popover.hide()
            else:
                popover.show_all()

    def _restore_state(self):
        """Restore window position."""
        x, y = Settings.get_default().window_position
        if x and y:
            # Move to x,y
            self.move(x, y)
        else:
            # Otherwise, center on screen
            self.set_position(Gtk.WindowPosition.CENTER)

    def close(self, *args):
        """Close the window."""
        # Save window position
        Settings.get_default().window_position = self.get_position()
        self.destroy()
