from gi.repository import GLib
from IconRequests.modules.settings import Settings
from IconRequests.modules.repos import Repositories
SUPPORTED_ICONS = []

settings = Settings.new()
repositories = Repositories()

# This is only needed for verifing if the issue already exists!
# Which means that the application will fetch the latest 400 open issues.
ISSUES_PER_PAGE = 100
NB_PAGES = 4

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
