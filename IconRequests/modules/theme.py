from glob import glob
from os import path
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk

from IconRequests.const import ICONS_DIRS


class Theme(Gtk.IconTheme):
    """Easy way to create new themes based on the theme name."""
    instance = None

    def __init__(self, theme_name):
        self._name = theme_name
        Gtk.IconTheme.__init__(self)
        self.set_custom_theme(self.name)
        self._get_supported_icons()

    @staticmethod
    def get_default():
        """Return the default theme."""
        if Theme.instance is None:
            theme_name = Gtk.Settings.get_default().props.gtk_icon_theme_name
            Theme.instance = Theme(theme_name)
        return Theme.instance

    @property
    def name(self):
        """Property: name."""
        return self._name

    def has_icon(self, icon_name):
        return icon_name in self._icons

    def _get_supported_icons(self):
        """Don't fallback."""
        subdirs = []
        icons_dirs = ["apps", "applications", "web"]
        size_dirs = ["48", "48x48", "scalable"]
        for size in size_dirs:
            for icon_dir in icons_dirs:
                subdirs.append("{}/{}/".format(size, icon_dir))
                subdirs.append("{}/{}/".format(icon_dir, size))
        icons = []
        folder_icons = []
        extensions = [".svg", ".png", ".xpm"]
        for icon_path in ICONS_DIRS:
            for icon_size in subdirs:
                icons_dir = path.join(icon_path, self.name, icon_size)
                if path.exists(icons_dir):
                    for ext in extensions:
                        icons = glob("{}*{}".format(icons_dir,
                                                    ext))
                        folder_icons.extend(icons)
                    for icon in folder_icons:
                        icon = path.basename(icon)
                        # Remove the extension
                        icon = path.splitext(icon)[0]
                        if icon not in icons:
                            icons.append(icon)
                folder_icons = []
        self._icons = icons

    def __getattr__(self, item):
        if isinstance(self.name, dict):
            return self.name[item]

    def __repr__(self, *args):
        return self.name
