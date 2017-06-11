from gettext import gettext as _
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk


class AboutDialog(Gtk.AboutDialog):

    def __init__(self):
        Gtk.AboutDialog.__init__(self)
        self.set_modal(True)
        self._build_widget()

    def _build_widget(self):
        self.set_authors(["Bilal Elmoussaoui"])
        self.set_logo_icon_name("icon-requests")
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_program_name(_("Icon Requests"))
        self.set_translator_credits(_("translator-credits"))
        self.set_version("1.0")
        self.set_comments(
            _("Simple application to report missing icons to github repository"))
        self.set_website("https://github.com/bil-elmoussaoui/Icon-Requests")
