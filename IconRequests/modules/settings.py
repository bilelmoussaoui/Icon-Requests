from gi.repository import Gio, GLib


class Settings(Gio.Settings):
    _instance = None
    def __init__(self):
        Gio.Settings.__init__(self)

    def new():
        gsettings = Gio.Settings.new("org.gnome.IconRequests")
        gsettings.__class__ = Settings
        return gsettings

    @staticmethod
    def get_default():
        if Settings._instance is None:
            Settings._instance = Settings.new()
        return Settings._instance

    @property
    def window_position(self):
        return tuple(self.get_value('window-position'))

    @window_position.setter
    def window_position(self, position):
        position = GLib.Variant('ai', list(position))
        self.set_value('window-position', position)

    @property
    def night_mode(self):
        return self.get_boolean('night-mode')

    @night_mode.setter
    def night_mode(self, state):
        self.set_boolean('night-mode', state)

    @property
    def imgur_client_id(self):
        return self.get_string("imgur-client-id")
