import requests
from os import path, makedirs, remove
from gi.repository import Gio, GLib
from json import loads, load, dump
from urllib.parse import urlsplit, urlencode

from IconRequests.const import ISSUES_PER_PAGE, NB_PAGES
from IconRequests.modules.log import Logger
from IconRequests.utils import load_from_resource


class Repositories:
    _instance = None
    _issues = None

    def __init__(self, theme):
        try:

            self._theme = theme
            self._repositories = loads(load_from_resource("repos.json"))
            self._get_supported_themes()
        except GLib.Error:
            Logger.error("Error loading repository database file. Exiting")
            exit()

    @staticmethod
    def get_default(theme):
        if Repositories._instance is None:
            Repositories._instance = Repositories(theme)
        return Repositories._instance

    @property 
    def is_supported(self):
        return self._theme in self._supported_themes

    def get_repo(self):
        url = self.get_url()
        if url:
            return urlsplit(url).path.strip("/")
        return None

    def get_url(self):
        key = self._get_key()
        if key:
            return self._repositories[key]["url"]
        return None

    def has_issue(self, app_name, app_icon):
        for issue in self.issues:
            title = issue.get("title", "").lower()
            body = issue.get("body", "")
            if app_icon in body or app_name in title:
                # Return the issue url
                return issue["html_url"]
        return None

    @property
    def issues(self):
        if self._issues is None and self.is_supported:
            self._issues = self._get_issues()
        return self._issues

    def _get_issues(self):
        repo = self.get_repo()
        cache_file = path.join(GLib.get_user_cache_dir(),
                               "IconRequests",
                               "{}.json".format(repo.replace("/", "-"))
                               )
        cache_dir = path.dirname(cache_file)
        # Create cache directory
        makedirs(cache_dir, exist_ok=True)

        issues_list = []
        url_data = {
            "state": "open",
            "per_page": str(ISSUES_PER_PAGE),
            "page": "1"
        }
        base_uri = "https://api.github.com/repos/{}/issues?".format(repo)
        for page in range(1, NB_PAGES + 1):
            url_data["page"] = str(page)
            try:
                query = requests.get(base_uri + urlencode(url_data))
                issues_list.extend(query.json())
            except requests.exceptions.ConnectionError:
                issues_list = []
                break
        if issues_list and not isinstance(issues_list[0], str):
            if path.exists(cache_file):
                remove(cache_file)
            with open(cache_file, 'w') as file_object:
                dump(issues_list, file_object, sort_keys=True, indent=4)
            file_object.close()
        else:
            if path.exists(cache_file):
                with open(cache_file, 'r') as file_object:
                    issues_list = load(file_object)
                file_object.close()
        return issues_list

    def _get_key(self):
        for key in self._repositories:
            if self._theme in key:
                return key
        return None

    def _get_supported_themes(self):
        supported = []
        for key in self._repositories:
            supported.extend(key.split(","))
        self._supported_themes = list(map(lambda x: x.strip(), supported))
