from gi.repository import Gio, GLib
from json import loads
import logging

class Repositories:

    def __init__(self):
        try:
            repos_obj = Gio.File.new_for_uri('resource:///org/gnome/IconRequests/repos.json')
            self._repositories = loads(str(repos_obj.load_contents(None)[1].decode("utf-8")))
        except GLib.Error as exception:
            logging.error(str(exception))
            exit()

    def is_supported(self, theme):
        return theme in self._repositories["reposlist"]

    def get_repo(self, theme):
        return self._repositories["repos"][theme]["repo"]

    def get_url(self, theme):
        return self._repositories["repos"][theme]["url"]

