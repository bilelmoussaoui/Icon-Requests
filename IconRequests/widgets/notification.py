from gettext import gettext as _
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class Notification(Gtk.Revealer):
    _timer = 0

    def __init__(self, message="", timeout=5):
        Gtk.Revealer.__init__(self)
        self.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self._message = message
        self._timeout = timeout
        self._build_widget()
        GLib.timeout_add_seconds(1, self._update_timer)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
        self._message_label.set_text(message)
        self._timer = 0

    def _build_widget(self):
        self._infobar = Gtk.InfoBar()
        self._infobar.connect("response", self._response)
        self._infobar.set_show_close_button(True)
        self._infobar.set_message_type(Gtk.MessageType.INFO)

        content_area = self._infobar.get_content_area()

        self._message_label = Gtk.Label()
        self._message_label.set_halign(Gtk.Align.START)
        self._message_label.set_text(self.message)

        content_area.add(self._message_label)
        self.add(self._infobar)

    @property
    def type(self):
        return self._infobar.get_message_type()

    @type.setter
    def type(self, message_type):
        self._infobar.set_message_type(message_type)

    def show(self):
        self.set_reveal_child(True)
        GLib.timeout_add_seconds(1, self._update_timer)

    def hide(self):
        self.set_reveal_child(False)

    def _response(self, infobar, response_id):
        if response_id == Gtk.ResponseType.CLOSE:
            self.hide()

    def _update_timer(self):
        if self.get_reveal_child():
            if self._timer == self._timeout:
                self.hide()
                self._timer = 0
            else:
                self._timer += 1
            return True
        return False
