from gi.repository import Gio, GLib
from json import loads
from urllib.parse import urlsplit
import logging

class Repositories:

    def __init__(self):
        try:
            repos_obj = Gio.File.new_for_uri('resource:///org/gnome/IconRequests/repos.json')
            self._repositories = loads(str(repos_obj.load_contents(None)[1].decode("utf-8")))
            self._get_supported_themes()
        except GLib.Error:
            logging.error("Error loading repository database file. Exiting")
            exit()

    def is_supported(self, theme):
        return theme in self._supported_themes

    def get_repo(self, theme):
        url = self.get_url(theme)
        return urlsplit(url).path.strip("/")

    def get_url(self, theme):
        key = self._get_key(theme)
        return self._repositories[key]["url"]

    def _get_key(self, theme):
        for key in self._repositories:
            if theme in key:
                return key
        return None

    def _get_supported_themes(self):
        supported = []
        for key in self._repositories:
            supported.extend(key.split(","))
        supported = list(map(lambda x: x.strip(), supported))
        self._supported_themes = supported
