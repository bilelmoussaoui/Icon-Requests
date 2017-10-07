from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk


from .row import ApplicationRow

class ApplicationsList(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self._build_widget()
        self.show_all()

    def _build_widget(self):
        self._listbox = Gtk.ListBox()
        self._listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.add_with_viewport(self._listbox)

    @property
    def listbox(self):
        return self._listbox

    def append(self, desktop_file):
        self._listbox.add(ApplicationRow(desktop_file))
