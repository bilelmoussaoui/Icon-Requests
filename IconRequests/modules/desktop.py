from IconRequests.const import SUPPORTED_ICONS
from configparser import ConfigParser, NoOptionError, RawConfigParser, DuplicateOptionError
from os import path, listdir
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib


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
        except (UnicodeDecodeError, DuplicateOptionError) as e:
            print(e)
            raise DesktopFileCorrupted
        try:
            self.path = "/".join(self.file.split("/")[:-1]) + "/"
            self.icon_name = config.get("Desktop Entry", "Icon").strip()
            self.get_icon_informations()
            self.name = config.get("Desktop Entry", "Name").strip()
            self.desktop_file = path.basename(self.file)
            self.description = config.get("Desktop Entry", "Comment", fallback="")
            self.path = "/".join(self.file.split("/")[:-1]) + "/"
        except (KeyError, NoOptionError):
            raise DesktopFileCorrupted

    def get_is_supported(self):
        icon_name = path.splitext(path.basename(self.icon_name))[0]
        return icon_name in SUPPORTED_ICONS

    def get_icon_informations(self):
        theme = Gtk.IconTheme.get_default()
        self.is_hardcoded_icon()
        self.icon_path = ""
        icon_name = self.icon_name
        self.is_supported = self.get_is_supported()
        full_path = False
        if self.is_hardcoded:
            self.icon_path = icon_name
            if len(self.icon_path.split("/")) == 1:
                icon_name = path.splitext(self.icon_name)[0]
            else:
                self.icon_path = self.icon_name
                full_path = True

        icon = theme.lookup_icon(icon_name, 48, 0)
        if icon and not full_path:
            self.icon_path = icon.get_filename()
            if self.is_hardcoded:
                self.is_supported = True

        if not self.icon_path or not path.exists(self.icon_path):
            self.icon_path = theme.lookup_icon(
                "image-missing", 48, 0).get_filename()

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
