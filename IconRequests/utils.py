from os import path, remove
from gi import require_version
from shutil import copyfile
require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gio, GLib


def copy_file(src, destination, overwrite=False):
    """
    Simple copy file function with the possibility to overwrite the file.
    Args :
        src(str) : source file
        dest(str) : destination folder
        overwrite(bool) : True to overwrite the file False by default
    """
    if overwrite:
        if path.isfile(destination):
            remove(destination)
        copyfile(src, destination)
    else:
        if not path.isfile(destination):
            copyfile(src, destination)


def is_gnome():
    """
        Check if the current desktop env is gnome
    """
    return GLib.getenv("XDG_CURRENT_DESKTOP").lower() == "gnome"


def is_app_menu():
    """
    Check if the top application menu is enabled or not.
    """
    default = True
    try:
        gsettings = Gio.Settings.new(
            'org.gnome.settings-daemon.plugins.xsettings')
        overrides = gsettings.get_value('overrides')['Gtk/ShellShowsAppMenu']
        show_app_menu = not bool(GLib.Variant.new_int32(overrides))
    except Exception:
        show_app_menu = default
    return show_app_menu


def get_icon(icon_path):
    """
        Generate a GdkPixbuf image
        :param image: icon name or image path
        :return: GdkPixbux Image
    """
    image = Gtk.Image()
    try:
        if "symbolic" in icon_path:
            icon_name = path.basename(icon_path).replace(".svg", "")
            image.set_from_gicon(Gio.ThemedIcon(name=icon_name),
                                 Gtk.IconSize.DIALOG)
        else:
            icon = GdkPixbuf.Pixbuf.new_from_file(icon_path)
            # Scale the icon down to avoid huge icons showing up
            if icon.get_width() != 48 or icon.get_height() != 48:
                icon = icon.scale_simple(48, 48,
                                         GdkPixbuf.InterpType.BILINEAR)
            image.set_from_pixbuf(icon)
    except GLib.Error:
        image.set_from_icon_name("image-missing",
                                 Gtk.IconSize.DIALOG)
    return image


def load_from_resource(filename):
    filename = "resource:///org/gnome/IconRequests/" + filename
    obj = Gio.File.new_for_uri(filename)
    content = str(obj.load_contents(None)[1].decode("utf-8"))
    return content
