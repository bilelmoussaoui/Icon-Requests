from IconRequests.utils import get_issues_list
from IconRequests.const import repositories
from xdg.DesktopEntry import DesktopEntry
from os import path, listdir
from json import loads
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib


class DesktopFile(DesktopEntry):

    def __init__(self, _file, upload_service, supported_icons):
        if not path.exists(_file):
            raise DesktopFileNotFound
        DesktopEntry.__init__(self, filename=_file)
        self.upload_service = upload_service
        self.desktop_file = path.basename(_file)
        self.supported_icons = supported_icons
        self.path = _file.replace(self.desktop_file, "")
        self.issue_url = None
        self.get_icon_informations()

    def get_is_supported(self):
        extensions = [".svg", ".png", ".xpm"]
        icon_name = path.basename(self.getIcon())
        for ext in extensions:
            icon_name = icon_name.replace(ext, "")
        return icon_name in self.supported_icons

    def get_icon_informations(self):
        theme = Gtk.IconTheme.get_default()
        self.is_hardcoded_icon()
        self.icon_path = ""
        icon_name = self.getIcon()
        self.is_supported = self.get_is_supported()
        self.supported_icons = None
        full_path = False
        if self.is_hardcoded:
            self.icon_path = icon_name
            if len(self.icon_path.split("/")) == 1:
                icon_name = path.splitext(self.getIcon())[0]
            else:
                self.icon_path = self.getIcon()
                full_path = True

        icon = theme.lookup_icon(icon_name, 48, 0)
        if icon and not full_path:
            self.icon_path = icon.get_filename()
            if self.is_hardcoded:
                self.is_supported = True

        if not self.icon_path or not path.exists(self.icon_path):
            icon = theme.lookup_icon(
                "image-missing", 48, 0)
            if icon:
                self.icon_path = icon.get_filename()

    def is_hardcoded_icon(self):
        img_exts = ["png", "svg", "xpm"]
        icon_path = self.getIcon().split("/")
        ext = path.splitext(self.getIcon())[1].strip(".")
        is_hardcoded = False
        if ext.lower() in img_exts or len(icon_path) > 1:
            is_hardcoded = True
        self.is_hardcoded = is_hardcoded

    def upload(self):
        """ Upload the missing icon to the current image service"""
        theme = Gio.Settings.new("org.gnome.desktop.interface").get_string("icon-theme")
        try:
            repo = repositories.get_repo(theme)
        except KeyError:
            raise ThemeNotSupported
            return False
        issues_list = get_issues_list(repo)
        issue_url = None
        app_name = self.getName().lower()
        app_icon = self.icon_path
        if len(issues_list) > 0 and issues_list[0].get("message", None):
            raise APIRateLimit
            return False
        else:
            for issue in issues_list:
                title = issue.get("title", "").lower()
                body = issue.get("body", "")
                if app_icon in body or app_name in title or app_name in body.lower():
                    issue_url = issue["html_url"]
                    break
        if not issue_url:
            self.icon_url = self.upload_service.upload(self.icon_path, self.getName())
            return True
        else:
            Gio.app_info_launch_default_for_uri(issue_url)
            return False

    def report(self):
        # TODO : use glib instead of wewbbrowser
        theme = Gio.Settings.new(
            "org.gnome.desktop.interface").get_string("icon-theme")
        if repositories.is_supported(theme):
            issue_model_obj = Gio.File.new_for_uri(
                'resource:///org/gnome/IconRequests/issue.model')
            issue_model = str(issue_model_obj.load_contents(None)[1].decode("utf-8"))
            repo_url = repositories.get_url(theme)
            issue_title = "Icon Request : %s" % self.getName()
            issue_model = issue_model.replace(
                "{app.name}", self.getName())
            issue_model = issue_model.replace(
                "{app.icon}", self.getIcon())
            issue_model = issue_model.replace(
                "{app.icon_url}", self.icon_url)
            issue_model = issue_model.replace(
                "{app.desktop}", self.desktop_file)
            issue_model = issue_model.replace("{theme}", theme)
            issue_model = issue_model.replace("\n", "%0A")
            url = "%s/issues/new?title=%s&body=%s" % (
                repo_url, issue_title, issue_model)
            Gio.app_info_launch_default_for_uri(url)
        else:
            raise ThemeNotSupported


class APIRateLimit(Exception):

    def __init__(self):
        super(APIRateLimit, self).__init__()


class ThemeNotSupported(Exception):

    def __init__(self):
        super(ThemeNotSupported, self).__init__()


class DesktopFileNotFound(Exception):

    def __init__(self):
        super(DesktopFileNotFound, self).__init__()


class DesktopFileCorrupted(Exception):

    def __init__(self):
        super(DesktopFileCorrupted, self).__init__()


class DesktopFileInvalid(Exception):

    def __init__(self):
        super(DesktopFileInvalid, self).__init__()
