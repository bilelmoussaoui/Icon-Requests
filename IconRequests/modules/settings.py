import logging
from gi.repository import Gio, GLib


class Settings(Gio.Settings):

    def __init__(self):
        Gio.Settings.__init__(self)

    def new():
        gsettings = Gio.Settings.new("org.gnome.IconRequests")
        gsettings.__class__ = Settings
        return gsettings

    def get_window_position(self):
        x, y = tuple(self.get_value('window-position'))
        return x, y

    def set_window_postion(self, position):
        position = GLib.Variant('ai', list(position))
        self.set_value('window-position', position)

    def set_is_night_mode(self, statue):
        self.set_boolean('night-mode', statue)

    def get_is_night_mode(self):
        return self.get_boolean('night-mode')

    def get_imgur_client_id(self):
        return self.get_string("imgur-client-id")
