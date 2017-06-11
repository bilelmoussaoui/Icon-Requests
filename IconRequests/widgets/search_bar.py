from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class SearchBar(Gtk.Revealer):

    def __init__(self):
        Gtk.Revealer.__init__(self)

        self._toggle_button = None
        self._search_list = []

        self.set_reveal_child(False)
        self._build_widgets()

    def connect_button(self, toggle_button):
        self._toggle_button = toggle_button
        self._toggle_button.connect("toggled", self._do_reveal)

    def add_data_source(self, listbox):
        if isinstance(listbox, list):
            self._search_list = listbox
        else:
            self._search_list = [listbox]

    def _build_widgets(self):
        self._entry = Gtk.SearchEntry()
        self._entry.connect("search-changed", self._do_search, self._filter)

        self.add(self._entry)

    def _do_search(self, search_entry, filter_function):
        data = search_entry.get_text().strip()
        for search_list in self._search_list:
            search_list.set_filter_func(filter_function, data, False)

    def _filter(self, row, data, notify_destroy):
        """Filter function."""
        search_data = row.get_search_data()
        data = data.lower()
        if data:
            return data in search_data.lower()
        else:
            return True

    def _do_reveal(self, toggle_button):
        is_active = toggle_button.props.active
        self.set_reveal_child(is_active)
        if is_active:
            self._entry.grab_focus_without_selecting()
        else:
            self._entry.set_text("")
            self._do_search(self._entry, lambda x, y, z: True)
