from configparser import ConfigParser, NoOptionError, RawConfigParser, DuplicateOptionError
from os import path, listdir
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

PIXMAPS_PATHS = ["/usr/share/pixmaps/",
                 "/usr/local/share/pixmaps/"]

class DesktopFile(object):

    def __init__(self, _file):
        if not path.exists(_file):
            raise DesktopFileNotFound
        self.file = _file
        self.read()

    @property
    def icon_name(self):
        return self._icon_name

    @icon_name.setter
    def icon_name(self, icon_name):
        self._icon_name = icon_name

    @property
    def name(self):
        return self._name

    @name.setter   
    def name(self, name):
        self._name = name

    def read(self):
        config = ConfigParser()
        try:
            config.read(self.file)
        except (UnicodeDecodeError, DuplicateOptionError):
            raise DesktopFileCorrupted
        try:
            try:
                visible = config.get("Desktop Entry", "NoDisplay")
                if bool(visible == "true"):
                    raise DesktopFileInvalid
            except (KeyError, NoOptionError):
                pass
            self.path = "/".join(self.file.split("/")[:-1]) + "/"
            self.icon_name = config.get("Desktop Entry", "Icon").strip()
            self.get_icon_informations()
            self.name = config.get("Desktop Entry", "Name").strip()
            self.desktop_file = path.basename(self.file)
            try:
                self.description = config.get("Desktop Entry", "Comment")
            except (KeyError, NoOptionError):
                self.description = ""
            self.path = "/".join(self.file.split("/")[:-1]) + "/"
        except (KeyError, NoOptionError):
            raise DesktopFileCorrupted

    def get_icon_informations(self):
        theme = Gtk.IconTheme()
        theme_name = Gio.Settings.new("org.gnome.desktop.interface").get_string("icon-theme")
        theme.set_custom_theme(theme_name)
        self.is_in_pixmaps = False
        self.is_hardcoded_icon()
        self.icon_path = ""
        if self.is_hardcoded:
            theme.append_search_path("/usr/share/pixmaps/")
        icon = theme.lookup_icon(self.icon_name, 48, 0)
        if self.is_hardcoded:
            self.icon_path = self.icon_name
            if len(self.icon_path.split("/")) == 1:
                if icon:
                    self.icon_path = icon.get_filename()
            if not path.exists(self.icon_path):
                self.icon_path = None
        else:
            if icon:
                self.icon_path = icon.get_filename()
            else:
                for pixmaps_path in PIXMAPS_PATHS:
                    if path.exists(pixmaps_path):
                        for icon in listdir(pixmaps_path):
                            if path.basename(icon) == path.basename(self.icon_name):
                                self.icon_path = pixmaps_path + self.icon_name
                                self.is_in_pixmaps = True
                                break
                    if self.is_in_pixmaps:
                        break
        if not self.icon_path:
            self.icon_path = theme.lookup_icon("image-missing", 48, 0).get_filename()
        self.is_supported = self.icon_name in theme.list_icons("Applications")

    def is_hardcoded_icon(self):
        img_exts = ["png", "svg", "xpm"]
        icon_path = self.icon_name.split("/")
        ext = path.splitext(self.icon_name)[1].strip(".")
        is_hardcoded = False
        if ext.lower() in img_exts or len(icon_path) > 1:
            is_hardcoded = True
        if "-symbolic" in self.icon_name.lower():
            is_hardcoded = True
        self.is_hardcoded = is_hardcoded


class DesktopFileNotFound(Exception):

    def __init__(self):
        super(DesktopFileNotFound, self).__init__()

class DesktopFileCorrupted(Exception):
    def __init__(self):
        super(DesktopFileCorrupted, self).__init__()

class DesktopFileInvalid(Exception):
    def __init__(self):
        super(DesktopFileInvalid, self).__init__()