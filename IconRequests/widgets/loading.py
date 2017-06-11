from gettext import gettext as _
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk


class Loading(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self._build_widgets()

    def _build_widgets(self):
        self._spinner = Gtk.Spinner()

        self._label = Gtk.Label()
        self._label.get_style_context().add_class("loading-label")

        self.pack_start(self._spinner, False, False, 6)
        self.pack_start(self._label, False, False, 6)

    @property
    def label(self):
        return self._label.get_text()

    @label.setter
    def label(self, value):
        self._label.set_text(_("{}...".format(value)))

    def start(self):
        self._spinner.start()

    def stop(self):
        self._spinner.stop()
