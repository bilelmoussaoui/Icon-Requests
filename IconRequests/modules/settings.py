import logging
from gi.repository import Gio


class Settings(Gio.Settings):

    def __init__(self):
        Gio.Settings.__init__(self)

    def new():
        gsettings = Gio.Settings.new("org.gnome.IconRequests")
        gsettings.__class__ = Settings
        return gsettings

    def get_window_position(self):
        x, y = self.get_int('position-x'), self.get_int('position-y')
        return x, y

    def set_window_postion(self, position):
        x, y = position
        self.set_int('position-x', x)
        self.set_int('position-y', y)

    def set_is_night_mode(self, statue):
        self.set_boolean('night-mode', statue)

    def get_is_night_mode(self):
        return self.get_boolean('night-mode')

    def get_imgur_client_id(self):
        return self.get_string("imgur-client-id")
