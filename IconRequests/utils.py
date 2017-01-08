from configparser import ConfigParser, NoOptionError, RawConfigParser
from os import listdir, path, getuid, environ as env
from gi import require_version
from pwd import getpwuid
require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gio
from subprocess import Popen, PIPE
from collections import OrderedDict
from shutil import copyfile
from IconRequests.modules.upload.imgur import imgur_upload_img


def get_info_from_dsktp_file(desktop_file):
    config = ConfigParser()
    try:
        config.read(desktop_file)
        desktop_infos = {}
        try:
            icon_name = config.get("Desktop Entry", "Icon")
            icon_info = get_icon_informations(icon_name)
            is_hardcoded = icon_info[3]
            is_in_pixmaps = icon_info[2]
            icon_path = icon_info[0]
            is_supported = icon_info[1]
            desktop_infos["icon"] = icon_name
            desktop_infos["is_hardcoded"] = is_hardcoded
            desktop_infos["is_supported"] = is_supported
            desktop_infos["is_in_pixmaps"] = is_in_pixmaps
            desktop_infos["icon_path"] = icon_path
            desktop_infos["name"] = config.get("Desktop Entry", "Name")
            desktop_infos["desktop"] = path.basename(desktop_file)
            desktop_infos["description"] = config.get(
                "Desktop Entry", "Comment")
            desktop_infos[
                "path"] = "/".join(desktop_file.split("/")[:-1]) + "/"
            return desktop_infos
        except (KeyError, NoOptionError):
            return False
    except FileNotFoundError:
        return False


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


def change_icon_name(desktop_file, icon_name):
    config = RawConfigParser()
    config.read(desktop_file)
    config.set("Desktop Entry", "Icon", icon_name)


def get_theme_name():
    gsettings = Gio.Settings.new("org.gnome.desktop.interface")
    return str(gsettings.get_value("icon-theme")).strip("'")


def list_supported_icons():
    theme_name = get_theme_name()
    if theme_name.lower() in ["numix-square", "numix-circle"]:
        icon_size = "48"
    else:
        icon_size = "48x48"
    icons = []
    for icon_path in ICONS_PATHS:
        if path.exists(icon_path + theme_name):
            icons.extend(listdir("%s/%s/apps/" %
                                 (icon_path + theme_name, icon_size)))
    icons = list(set(icons))
    icons = [icon.replace(".svg", "") for icon in icons]
    icons.sort()
    return icons


def get_icon_informations(icon_name):
    theme = Gtk.IconTheme.get_default()
    is_supported = False
    is_in_pixmaps = False
    is_hardcoded = is_hardcoded_icon(icon_name)
    icon_path = ""
    icon = theme.lookup_icon(icon_name, 48, 0)
    if is_hardcoded:
        icon_path = icon_name
        if len(icon_path.split("/")) == 1:
            if icon:
                icon_path = icon.get_filename()
    else:
        if icon:
            icon_path = icon.get_filename()
        else:
            for pixmaps_path in PIXMAPS_PATHS:
                for icon in listdir(pixmaps_path):
                    if path.basename(icon) == path.basename(icon_name):
                        icon_path = pixmaps_path + icon_name
                        is_in_pixmaps = True
                        break
                if is_in_pixmaps:
                    break
    if not icon_path:
        icon_path = theme.lookup_icon("image-missing", 48, 0).get_filename()
    is_supported = icon_name in SUPPORTED_ICONS
    return icon_path, is_supported, is_in_pixmaps, is_hardcoded


def is_gnome():
    """
        Check if the current distro is gnome
    """
    return env.get("XDG_CURRENT_DESKTOP").lower() == "gnome"


def get_user_destkop():
    p = Popen(["xdg-user-dir", "DESKTOP"], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output.decode("utf-8").strip() + "/"


def get_username():
    return getpwuid(getuid())[0]

ICONS_PATHS = ["/usr/share/icons/",
               "/usr/local/share/icons/",
               "/home/%s/.local/share/icons/" % get_username()]
PIXMAPS_PATHS = ["/usr/share/pixmaps/",
                 "/usr/local/share/pixmaps/"]

DESKTOP_FILE_DIRS = ["/usr/share/applications/",
                     "/usr/share/applications/kde4/",
                     "/usr/local/share/applications/",
                     "/usr/local/share/applications/kde4/"
                     "/home/%s/.local/share/applications/" % get_username(),
                     "/home/%s/.local/share/applications/kde4/" % get_username(),
                     get_user_destkop()]

IGNORE_FILES = ["defaults.list", "mimeapps.list", "mimeinfo.cache"]

SUPPORTED_ICONS = list_supported_icons()


def is_hardcoded_icon(icon_name):
    img_exts = ["png", "svg", "xpm"]
    icon_path = icon_name.split("/")
    ext = path.splitext(icon_name)[1]
    is_hardcoded = False
    if ext.lower() in img_exts or len(icon_path) > 1:
        is_hardcoded = True
    if "-symbolic" in icon_name:
        is_hardcoded = True
    return is_hardcoded


def get_desktop_files_info():
    global DESKTOP_FILE_DIRS, IGNORE_FILES
    desktop_files = {}
    already_added = []
    for desktop_dir in DESKTOP_FILE_DIRS:
        if path.isdir(desktop_dir):
            all_files = listdir(desktop_dir)
            for desktop_file in all_files:
                desktop_file_path = desktop_dir + desktop_file
                ext = path.splitext(desktop_file)[1].lower().strip(".")
                if desktop_file and desktop_file not in IGNORE_FILES:
                    if ext == "desktop" and desktop_file not in already_added:
                        already_added.append(desktop_file)
                        desktop_info = get_info_from_dsktp_file(
                            desktop_file_path)
                        if desktop_info:
                            desktop_files[desktop_file_path] = desktop_info
    data = OrderedDict(sorted(desktop_files.items(),
                              key=lambda x: x[1]["name"].lower()))
    return data


def upload_icon(icon_path, app_name):
    icon_extension = path.splitext(icon_path)[1].lower().strip(".")
    if icon_extension == "png":
        icon_url = imgur_upload_img(icon_path, app_name)
        return icon_url
    return None


def get_icon(icon_path):
    """
        Generate a GdkPixbuf image
        :param image: icon name or image path
        :return: GdkPixbux Image
    """
    icon = GdkPixbuf.Pixbuf.new_from_file(icon_path)
    if icon.get_width() != 48 or icon.get_height() != 48:
        icon = icon.scale_simple(48, 48, GdkPixbuf.InterpType.BILINEAR)
    return icon
