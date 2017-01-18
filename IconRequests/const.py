from IconRequests.utils import get_supported_icons
from IconRequests.utils import get_username, get_user_destkop
from threading import Thread
SUPPORTED_ICONS = []


def run_thread():
    global SUPPORTED_ICONS
    SUPPORTED_ICONS = get_supported_icons()

load_icons_thread = Thread(target=run_thread())
load_icons_thread.daemon = True
load_icons_thread.start()

DESKTOP_FILE_DIRS = ["/usr/share/applications/",
                     "/usr/share/applications/kde4/",
                     "/usr/local/share/applications/",
                     "/usr/local/share/applications/kde4/",
                     "/home/%s/.local/share/applications/" % get_username(),
                     "/home/%s/.local/share/applications/kde4/" % get_username(),
                     get_user_destkop()]
