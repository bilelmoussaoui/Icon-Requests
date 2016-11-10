from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gio, GLib, Gdk, Pango
from gettext import gettext as _
import logging
import sys
from os import path
sys.path.insert(0, '../')
from utils import get_icon, get_theme_name
import webbrowser


class ApplicationRow(Gtk.ListBoxRow):
    def __init__(self, application, parent):
        self.applicaiton = application
        self.parent = parent
        Gtk.ListBoxRow.__init__(self)
        self.generate()

    def generate(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        image = Gtk.Image(xalign=0)
        image.set_from_pixbuf( get_icon(self.applicaiton["icon"]))
        image_box.pack_start(image, False, False, 6)

        name_label = Gtk.Label()
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_justify(Gtk.Justification.LEFT)
        name_label.set_text(self.applicaiton["name"])
        name_label.get_style_context().add_class("application-name")
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        name_box.add(name_label)
        info_box.pack_start(name_box, False, False, 6)

        path_label = Gtk.Label()
        path_label.set_justify(Gtk.Justification.LEFT)
        path_label.set_text(self.applicaiton["path"])
        path_label.set_ellipsize(Pango.EllipsizeMode.END)
        path_label.get_style_context().add_class("application-path")
        path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        path_box.add(path_label)
        info_box.pack_start(path_box, False, False, 6)

        fix_button = Gtk.Button()
        fix_button.set_label(_("Fix"))
        if not self.applicaiton["is_hardcoded"]:
            fix_button.set_sensitive(False)
        else:
            fix_button.get_style_context().add_class("suggested-action")
        fix_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        fix_box.add(fix_button)

        report_button = Gtk.Button()
        report_button.set_label(_("Report..."))
        report_button.connect("clicked", self.report_missing_icon)
        if self.applicaiton["is_supported"]:
            report_button.set_sensitive(False)
        else:
            report_button.get_style_context().add_class("suggested-action")
        report_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        report_box.add(report_button)

        main_box.pack_start(image_box, False, False, 6)
        main_box.pack_start(info_box, False, False, 6)
        main_box.pack_end(fix_box, False, False, 6)
        main_box.pack_end(report_box, False, False, 6)
        self.add(main_box)

    def get_name(self):
        return self.applicaiton["name"]

    def report_missing_icon(self, *args):
        with open("./data/issue.model") as f:
            issue_model = f.read()

        issue_title = "Icon Request : %s" % self.applicaiton["name"]
        issue_model = issue_model.replace("{app.name}", self.applicaiton["name"])
        issue_model = issue_model.replace("{app.icon}", self.applicaiton["icon"])
        issue_model = issue_model.replace("{app.desktop}", path.basename(self.applicaiton["desktop"]))
        issue_model = issue_model.replace("{theme}", get_theme_name())
        issue_model = issue_model.replace("\n", "%0A")
        url = "https://github.com/numixproject/numix-core/issues/new?title=%s&body=%s"% (issue_title, issue_model)
        webbrowser.open(url)
