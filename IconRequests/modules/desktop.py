from xdg.DesktopEntry import DesktopEntry
from os import path, listdir
from json import loads
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib

from IconRequests.modules.upload.imgur import Imgur
from IconRequests.modules.repos import Repositories
from IconRequests.modules.theme import Theme
from IconRequests.utils import load_from_resource


class DesktopFile(DesktopEntry):

    def __init__(self, _file):
        if not path.exists(_file):
            raise DesktopFileNotFound
        DesktopEntry.__init__(self, filename=_file)
        self._desktop_file = path.basename(_file)
        self._path = _file.replace(self._desktop_file, "")
        self._issue_url = None
        self._theme = Theme()
        self._parse_desktop_file()

    @property
    def path(self):
        return self._path

    @property
    def desktop_file(self):
        return self._desktop_file

    @property
    def icon_path(self):
        return self._icon_path

    @property
    def is_hardcoded(self):
        return self._is_hardcoded

    @property
    def is_supported(self):
        return self._is_supported

    def _parse_desktop_file(self):
        self._is_hardcoded = self.__is_hardcoded()
        self._is_supported = self._theme.has_icon(self.getIcon())
        self._get_icon_path()

    def _get_icon_path(self):
        self.supported_icons = None
        full_path = False
        icon_name = self.getIcon()
        self._icon_path = None
        if self._is_hardcoded:
            self._icon_path = icon_name
            if len(self._icon_path.split("/")) == 1:
                icon_name = path.splitext(self.getIcon())[0]
            else:
                self._icon_path = self.getIcon()
                full_path = True

        icon = self._theme.lookup_icon(icon_name, 48, 0)
        if icon and not full_path:
            self._icon_path = icon.get_filename()
            if self._is_hardcoded:
                self._is_supported = True

        if not self._icon_path or not path.exists(self._icon_path):
            icon = self._theme.lookup_icon("image-missing", 48, 0)
            if icon:
                self._icon_path = icon.get_filename()

    def __is_hardcoded(self):
        img_exts = ["png", "svg", "xpm"]
        icon_path = self.getIcon().split("/")
        ext = path.splitext(self.getIcon())[1].strip(".")
        is_hardcoded = False
        if ext.lower() in img_exts or len(icon_path) > 1:
            is_hardcoded = True
        return is_hardcoded

    def upload(self):
        """ Upload the missing icon to the current image service"""
        app_name = self.getName().lower()
        app_icon = self.getIcon()
        issue_url = Repositories.get_default(
            self._theme.name).has_issue(app_name, app_icon)
        if not issue_url:
            self._icon_url = Imgur.get_default().upload(self.icon_path, self.getName())
            return True

        Gio.app_info_launch_default_for_uri(issue_url)
        return False

    def report_hardcoded(self):
        repo_url = "https://github.com/Foggalong/hardcode-fixer"
        issue_title = self.getName()
        issue_model = load_from_resource("hardcode-fixer-issue.model")
        data = {
            "{app.name}": self.getName(),
            "{app.icon}": self.getIcon(),
            "{app.desktop}": self.desktop_file,
            "\n": "%0A"
        }
        for key, value in data.items():
            issue_model = issue_model.replace(key, value)
        url = "%s/issues/new?title=%s&body=%s" % (
            repo_url, issue_title, issue_model)
        Gio.app_info_launch_default_for_uri(url)

    def report(self):
        repos = Repositories.get_default(self._theme.name)
        if repos.is_supported():
            issue_model = load_from_resource("issue.model")
            issue_title = "Icon Request: {}".format(self.getName())
            repo_url = repos.get_url()
            data = {
                "{app.name}": self.getName(),
                "{app.icon}": self.getIcon(),
                "{app.icon_url}": self._icon_url,
                "{app.desktop}": self.desktop_file,
                "{theme}": self._theme.name,
                "\n": "%0A"
            }
            for key, value in data.items():
                issue_model = issue_model.replace(key, value)
            url = "%s/issues/new?title=%s&body=%s" % (
                repo_url, issue_title, issue_model)
            Gio.app_info_launch_default_for_uri(url)
