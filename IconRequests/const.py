from os import path
from gi.repository import GLib, Gio


App = Gio.Application.get_default


# This is only needed for verifing if the issue already exists!
# Which means that the application will fetch the latest 400 open issues.
ISSUES_PER_PAGE = 100
NB_PAGES = 4
DESKTOP_FILE_DIRS = [
    "/usr/share/applications/",
    "/usr/share/applications/kde4/",
    "/usr/share/applications/wine/",
    "/usr/local/share/applications/",
    "/usr/local/share/applications/kde4/",
    "/usr/local/share/applications/wine/",
    path.join(GLib.get_home_dir(), ".local/share/applications/"),
    path.join(GLib.get_home_dir(), ".local/share/applications/kde4/"),
    path.join(GLib.get_home_dir(), ".local/share/applications/wine/"),
    GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)
]

ICONS_DIRS = [
    path.join(GLib.get_home_dir(), '.icons'),
    path.join(GLib.get_home_dir(), '.local/share/icons'),
    '/usr/local/share/icons',
    '/usr/share/icons'
]

class ApplicationType:
    HARDCODED = "hardcoded"
    UNSUPPORTED = "unsupoorted"
    ALL = "all"
