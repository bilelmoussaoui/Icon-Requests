from threading import Thread
from gi.repository import GObject, Gio, GLib
from glob import glob
from IconRequests.const import DESKTOP_FILE_DIRS
from IconRequests.modules.desktop import DesktopFile
from IconRequests.widgets.applications.list import ApplicationsList
import xdg

class ApplicationsController(GObject.GObject):
    __gsignals__ = {
        'loaded': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'reload': (GObject.SignalFlags.RUN_FIRST, None, ()),
        "parse": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.connect("reload", self.start)
        self.start()

    def start(self, *args):
        self._db = []
        thread = Thread(target=self._parse_apps)
        thread.daemon = True
        thread.start()

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def _parse_apps(self):
        already_added = []
        database = []
        # theme = Gio.Settings.new("org.gnome.desktop.interface").get_string("icon-theme")
        for desktop_dir in DESKTOP_FILE_DIRS:
            files = glob("{}*.desktop".format(desktop_dir))
            for desktop_file in files:
                try:
                    obj = DesktopFile(desktop_file)
                    icon_name = obj.getIcon()
                    self.emit("parse", obj.getName())
                    if icon_name not in already_added:
                        database.append(obj)
                        already_added.append(icon_name)
                except xdg.Exceptions.ParsingError:
                    pass
        database = sorted(database, key=lambda x: x.getName().lower())
        self._db = database
        self.emit("loaded")

    @property
    def database(self):
        return self._db
