from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gio, GLib, Gdk, Pango
from gettext import gettext as _
import logging
from os import path
from IconRequests.widgets.search_bar import SearchBar
from IconRequests.utils import SUPPORTED_ICONS
from threading import Thread


class IconChooser(Gtk.Window,  Thread, GObject.GObject):
    __gsignals__ = {
        'icons_loaded': (GObject.SignalFlags.RUN_LAST, None, (bool,))
    }

    def __init__(self, parent, application):
        Thread.__init__(self)
        GObject.GObject.__init__(self)
        self.parent = parent
        self.daemon = True
        self.spinner = Gtk.Spinner()
        self.application = application
        self.search_button = Gtk.ToggleButton()
        self.generate_window()
        self.generate_components()
        self.start()

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def run(self):
        self.generate_flow_box_icons()
        self.emit("icons_loaded", True)

    def do_icons_loaded(self, *args):
        self.spinner.stop()
        self.spinner_box_outer.hide()
        self.scrolled_window.show()
        self.flowbox.hide()
        if len(self.flowbox.get_children()) != 0:
            self.flowbox.show_all()

    def generate_window(self):
        Gtk.Window.__init__(self, title=_("Icon Chooser"),
                            type=Gtk.WindowType.TOPLEVEL,
                            destroy_with_parent=True, modal=True)
        self.connect("delete-event", self.close_window)
        self.resize(400, 300)
        self.set_size_request(400, 300)
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_transient_for(self.parent)
        self.connect("key_press_event", self.on_key_press)

    def generate_components(self):
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.set_titlebar(self.hb)

        search_icon = Gio.ThemedIcon(name="system-search-symbolic")
        search_image = Gtk.Image.new_from_gicon(
            search_icon, Gtk.IconSize.BUTTON)
        self.search_button.set_tooltip_text(_("Search"))
        self.search_button.set_image(search_image)

        save_button = Gtk.Button()
        save_button.get_style_context().add_class("suggested-action")
        save_button.set_label(_("Save"))
        save_button.connect("clicked", self.change_icon_name)

        self.hb.pack_end(self.search_button)
        self.hb.pack_end(save_button)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.generate_flow_box()

        self.search_bar = SearchBar(
            self, self.search_button, [self.flowbox])

        self.spinner_box_outer = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL)
        spinner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.spinner.start()
        self.spinner.show()

        self.main_box.pack_start(self.search_bar, False, False, 0)
        self.main_box.pack_start(self.scrolled_window, True, True, 0)

        spinner_box.pack_start(self.spinner, False, False, 6)
        self.spinner_box_outer.pack_start(spinner_box, True, True, 6)
        self.main_box.pack_start(self.spinner_box_outer, True, True, 0)

        self.add(self.main_box)

    def generate_flow_box(self):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.hide()
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(12)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.scrolled_window.add(self.flowbox)

    def change_icon_name(self, *args):
        selected_row = self.flowbox.get_selected_children().get_children()[
            0]
        icon_name = selected_row.get_name()

    def generate_flow_box_icons(self):
        added_icons = []
        for icon in SUPPORTED_ICONS:
            self.flowbox.add(FlowBoxRow(icon))

    def show_window(self):
        self.show_all()

    def on_key_press(self, key, key_event):
        """
            Keyboard Listener handler
        """
        if Gdk.keyval_name(key_event.keyval) == "Escape":
            self.close_window()

    def close_window(self, *args):
        """
            Close the window
        """
        logging.debug("IconChoser closed")
        self.destroy()


class FlowBoxRow(Gtk.Box):

    def __init__(self, icon_name):
        self.icon_name = icon_name
        self.generate()

    def generate(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        flowbox_image = Gtk.Image.new_from_icon_name(
            self.icon_name, Gtk.IconSize.DIALOG)
        flowbox_image.set_tooltip_text(self.icon_name)
        self.add(flowbox_image)

    def get_name(self, *args):
        return self.icon_name
