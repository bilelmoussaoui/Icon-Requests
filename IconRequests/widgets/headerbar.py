from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf
from gettext import gettext as _


class HeaderBar(Gtk.HeaderBar):
    search_button = Gtk.ToggleButton()

    def __init__(self, window):
        self.window = window
        Gtk.HeaderBar.__init__(self)
        self.set_show_close_button(True)
        self.generate()
        self.show_all()

    def generate(self):
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)
        self.stack.set_transition_type(
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        search_icon = Gio.ThemedIcon(name="system-search-symbolic")
        search_image = Gtk.Image.new_from_gicon(
            search_icon, Gtk.IconSize.BUTTON)
        self.search_button.set_tooltip_text(_("Search"))
        self.search_button.set_image(search_image)
        self.set_custom_title(stack_switcher)
        self.pack_end(self.search_button)
