from gi.repository import GLib
from IconRequests.modules.settings import Settings
SUPPORTED_ICONS = []

settings = Settings.new()
DESKTOP_FILE_DIRS = ["/usr/share/applications/",
                     "/usr/share/applications/kde4/",
                     "/usr/share/applications/wine/",
                     "/usr/local/share/applications/",
                     "/usr/local/share/applications/kde4/",
                     "/usr/local/share/applications/wine/",
                     "%s/.local/share/applications/" % GLib.get_home_dir(),
                     "%s/.local/share/applications/kde4/" % GLib.get_home_dir(),
                     "%s/.local/share/applications/wine/" % GLib.get_home_dir(),
                     GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)]
