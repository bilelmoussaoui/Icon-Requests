from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gio, GLib, Gdk, Pango
from gettext import gettext as _
import logging
from os import path
from IconRequests.utils import get_icon, get_theme_name, change_icon_name, copy_file, upload_icon
from IconRequests.widgets.icon_choser import IconChooser
import webbrowser
from json import loads
from threading import Thread


class ApplicationRow(Gtk.ListBoxRow, Thread, GObject.GObject):
    __gsignals__ = {
        'icon_uploaded': (GObject.SignalFlags.RUN_LAST, None, (bool,))
    }

    def __init__(self, application, parent):
        Thread.__init__(self)
        GObject.GObject.__init__(self)
        Gtk.ListBoxRow.__init__(self)
        self.application = application
        self.parent = parent
        self.spinner = Gtk.Spinner()
        self.daemon = True
        self.generate()

    def generate(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        image = Gtk.Image(xalign=0)
        image.set_from_pixbuf(get_icon(self.application["icon_path"]))
        image_box.pack_start(image, True, False, 6)

        name_label = Gtk.Label()
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_justify(Gtk.Justification.LEFT)
        name_label.set_text(self.application["name"])
        name_label.get_style_context().add_class("application-name")
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        name_box.add(name_label)
        info_box.pack_start(name_box, False, False, 3)

        description_label = Gtk.Label()
        description_label.set_justify(Gtk.Justification.LEFT)
        description_label.set_text(self.application["description"])
        description_label.set_ellipsize(Pango.EllipsizeMode.END)
        description_label.get_style_context().add_class("application-label")
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label_box.add(description_label)
        info_box.pack_start(label_box, False, False, 3)

        path_label = Gtk.Label()
        path_label.set_justify(Gtk.Justification.LEFT)
        path_label.set_text(self.application["path"])
        path_label.set_ellipsize(Pango.EllipsizeMode.END)
        path_label.get_style_context().add_class("application-path")
        path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        path_box.add(path_label)
        info_box.pack_start(path_box, False, False, 3)
        if self.application["is_hardcoded"]:
            fix_button = Gtk.Button()
            fix_button.set_label(_("Fix"))
            fix_button.connect("clicked", self.fix_hardcoded_icon)
            fix_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                              valign=Gtk.Align.CENTER)
            fix_box.add(fix_button)
            main_box.pack_end(fix_box, False, False, 6)

        if not self.application["is_supported"]:
            report_button = Gtk.Button()
            report_button.set_label(_("Report"))
            report_button.connect("clicked", self.report_missing_icon)
            report_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
            report_box.add(report_button)
            main_box.pack_end(report_box, False, False, 6)

        main_box.pack_start(image_box, False, False, 6)
        main_box.pack_start(info_box, False, False, 6)
        self.add(main_box)

    def fix_hardcoded_icon(self, *args):
        icon_name = self.application["icon"]
        icon_extension = path.splitext(icon_name)[1].lower().strip(".")
        if icon_extension != "":
            new_icon_name = icon_name.split(
                "/")[-1].replace(".%s" % icon_extension, "")
            if new_icon_name.lower() in ["logo", "icon"]:
                new_icon_name = self.application["name"].lower()
            if icon_extension == "png":
                icon_path = "/usr/share/icons/hicolor/48x48/"
            elif icon_extension == "svg":
                icon_path = "/usr/share/icons/hicolor/scalable/"
            elif icon_extension == "xpm":
                icon_path = "/usr/share/pixmaps/"
            copy_file(icon_name, icon_path +
                      new_icon_name + "." + icon_extension)
            change_icon_name(self.application["path"] +
                             self.application["desktop"], new_icon_name)
        else:
            self.show_icon_choser()

    def show_icon_choser(self, *args):
        icon_choser = IconChooser(self.parent.parent, self.application)
        icon_choser.show_window()

    def get_name(self):
        return self.application["name"]

    def run(self):
        icon_path = self.application["icon_path"]
        app_name = self.application["name"]
        self.icon_url = upload_icon(icon_path, app_name)
        self.emit("icon_uploaded", True)

    def report_missing_icon(self, *args):
        self.start()

    def do_icon_uploaded(self, *args):
        theme = get_theme_name()
        repos_obj = Gio.File.new_for_uri(
            'resource:///org/gnome/IconRequests/repos.json')
        repositories = loads(str(repos_obj.load_contents(None)
                                 [1].decode("utf-8")))
        if theme in repositories.keys():
            issue_model_obj = Gio.File.new_for_uri(
                'resource:///org/gnome/IconRequests/issue.model')
            issue_model = str(issue_model_obj.load_contents(None)[
                              1].decode("utf-8"))
            repo_url = repositories[theme]
            issue_title = "Icon Request : %s" % self.application["name"]
            issue_model = issue_model.replace(
                "{app.name}", self.application["name"])
            issue_model = issue_model.replace(
                "{app.icon}", self.application["icon"])
            issue_model = issue_model.replace(
                "{app.icon_url}", self.icon_url)
            issue_model = issue_model.replace(
                "{app.desktop}", path.basename(self.application["desktop"]))
            issue_model = issue_model.replace("{theme}", theme)
            issue_model = issue_model.replace("\n", "%0A")
            url = "%s/issues/new?title=%s&body=%s" % (
                repo_url, issue_title, issue_model)
            webbrowser.open(url)
        else:
            print("show an info bar message please")
