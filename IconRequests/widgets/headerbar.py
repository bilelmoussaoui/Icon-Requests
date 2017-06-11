from gettext import gettext as _

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class HeaderBar(Gtk.HeaderBar):
    _instance = None

    def __init__(self):
        Gtk.HeaderBar.__init__(self)

        self.set_show_close_button(True)
        self._build_widget()

    @staticmethod
    def get_default():
        if HeaderBar._instance is None:
            HeaderBar._instance = HeaderBar()
        return HeaderBar._instance

    def _build_widget(self):
        self._stack_switcher = Gtk.StackSwitcher()
        self.set_custom_title(self._stack_switcher)

        self._search_button = HeaderToggleButton("system-search-symbolic",
                                                 _("Search"))
        self._menu_button = HeaderButton("open-menu-symbolic", None)
        self._menu_button.hide()

        self.pack_end(self._search_button)
        self.pack_end(self._menu_button)

    def set_stack(self, stack):
        self._stack_switcher.set_stack(stack)

    @property
    def search_button(self):
        return self._search_button

    @property
    def menu_button(self):
        return self._menu_button


class HeaderBarButton:

    def __init__(self, icon, tooltip):
        self._icon = icon
        self._tooltip = tooltip
        self._build_widget()

    def _build_widget(self):
        icon = Gio.ThemedIcon(name=self._icon)
        image = Gtk.Image.new_from_gicon(icon,
                                         Gtk.IconSize.BUTTON)
        self.set_image(image)
        self.set_tooltip_text(self._tooltip)

    def hide(self):
        self.set_visible(False)
        self.set_no_show_all(True)

    def show(self):
        self.set_visible(True)
        self.set_no_show_all(False)


class HeaderButton(Gtk.Button, HeaderBarButton):

    def __init__(self, icon, tooltip=""):
        Gtk.Button.__init__(self)
        HeaderBarButton.__init__(self, icon, tooltip)


class HeaderToggleButton(Gtk.ToggleButton, HeaderBarButton):

    def __init__(self, icon, tooltip=""):
        Gtk.ToggleButton.__init__(self)
        HeaderBarButton.__init__(self, icon, tooltip)

    def toggle(self):
        # Toggle the button only when it's visible
        if self.props.visible:
            is_active = self.get_active()
            self.set_active(not is_active)
