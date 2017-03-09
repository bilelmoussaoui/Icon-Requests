from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gio, GLib, Gdk, Pango
from gettext import gettext as _
import logging
from os import path
from IconRequests.modules.upload.upload import ConnexionError
from IconRequests.modules.desktop import ThemeNotSupported, APIRateLimit
from IconRequests.utils import get_icon, change_icon_name, copy_file
from threading import Thread


class ApplicationRow(Gtk.ListBoxRow, GObject.GObject):
    stack_name = None
    __gsignals__ = {
        'icon_uploaded': (GObject.SignalFlags.RUN_LAST, None, (bool,))
    }

    def __init__(self, desktop_file, notification):
        GObject.GObject.__init__(self)
        Gtk.ListBoxRow.__init__(self)
        self.desktop_file = desktop_file
        self.notification = notification
        self.spinner = Gtk.Spinner()
        self.generate()

    def generate(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        image = Gtk.Image(xalign=0)
        icon = get_icon(self.desktop_file.icon_path)
        if icon:
            if type(icon) == tuple:
                icon_name = path.basename(icon[1]).replace(".svg", "")
                image.set_from_gicon(Gio.ThemedIcon(name=icon_name),
                                     Gtk.IconSize.DIALOG)
            else:
                image.set_from_pixbuf(icon)
        else:
            image.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        image_box.pack_start(image, True, False, 6)

        name_label = Gtk.Label()
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_justify(Gtk.Justification.LEFT)
        name_label.set_text(self.desktop_file.getName())
        name_label.get_style_context().add_class("application-name")
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        name_box.add(name_label)
        info_box.pack_start(name_box, False, False, 3)

        description_label = Gtk.Label()
        description_label.set_justify(Gtk.Justification.LEFT)
        description_label.set_text(self.desktop_file.getComment())
        description_label.set_tooltip_text(self.desktop_file.getComment())
        description_label.set_ellipsize(Pango.EllipsizeMode.END)
        description_label.get_style_context().add_class("application-label")
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label_box.add(description_label)
        info_box.pack_start(label_box, False, False, 3)

        path_label = Gtk.Label()
        path_label.set_justify(Gtk.Justification.LEFT)
        file_path = path.join(self.desktop_file.path, self.desktop_file.desktop_file)
        path_label.set_text(file_path)
        path_label.set_tooltip_text(file_path)
        path_label.set_ellipsize(Pango.EllipsizeMode.END)
        path_label.get_style_context().add_class("application-path")
        path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        path_box.add(path_label)
        info_box.pack_start(path_box, False, False, 3)

        if not self.desktop_file.is_supported:
            self.spinner = Gtk.Spinner()
            self.spinner.set_visible(False)
            self.spinner.set_no_show_all(True)
            self.report_label = Gtk.Label()
            self.report_label.set_text(_("Report"))
            self.report_button = Gtk.Button()
            self.report_button.add(self.report_label)
            self.report_button.get_style_context().add_class("text-button")
            self.report_button.connect("clicked", self.report_missing_icon)
            report_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
            report_box.add(self.report_button)
            main_box.pack_end(report_box, False, False, 6)

        if self.desktop_file.is_hardcoded:
            self.fix_button = Gtk.Button()
            self.fix_label = Gtk.Label()
            self.fix_label.set_text(_("Fix"))
            self.fix_button.add(self.fix_label)
            self.fix_button.set_sensitive(False)
            self.fix_button.get_style_context().add_class("text-button")
            self.fix_button.set_tooltip_text("Not supported at the moment")
            self.fix_button.connect("clicked", self.fix_hardcoded_icon)
            fix_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                              valign=Gtk.Align.CENTER)
            fix_box.add(self.fix_button)
            main_box.pack_end(fix_box, False, False, 6)
            if not self.desktop_file.is_supported:
                self.report_button.set_sensitive(False)

        main_box.pack_start(image_box, False, False, 6)
        main_box.pack_start(info_box, False, False, 6)
        self.add(main_box)

    def fix_hardcoded_icon(self, *args):
        icon_name = self.desktop_file.getIcon()
        icon_extension = path.splitext(icon_name)[1].lower().strip(".")
        new_icon_name = icon_name.split(
            "/")[-1].replace(".%s" % icon_extension, "")
        if new_icon_name.lower() in ["logo", "icon"]:
            new_icon_name = self.desktop_file.getName().lower()
        if icon_extension == "png":
            icon_path = "/usr/share/icons/hicolor/48x48/"
        elif icon_extension == "svg":
            icon_path = "/usr/share/icons/hicolor/scalable/"
        elif icon_extension == "xpm":
            icon_path = "/usr/share/pixmaps/"
        copy_file(icon_name, icon_path +
                  new_icon_name + "." + icon_extension)
        change_icon_name(self.desktop_file.path +
                         self.desktop_file.desktop, new_icon_name)

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def run(self):
        upload_status = False
        try:
            upload_status = self.desktop_file.upload()
        except ConnexionError:
            self.notification.set_message(_("Please check your connexion"))
            self.notification.set_type(Gtk.MessageType.ERROR)
            self.notification.show()
        except ThemeNotSupported:
            self.notification.set_message(_("Theme not supported"))
            self.notification.set_type(Gtk.MessageType.ERROR)
            self.notification.show()
        except APIRateLimit:
            self.notification.set_message(_("You've reached your API limits"))
            self.notification.set_type(Gtk.MessageType.INFO)
            self.notification.show()
        self.emit("icon_uploaded", upload_status)

    def report_missing_icon(self, *args):
        self.report_button.set_sensitive(False)
        self.report_button.get_style_context().remove_class("text-button")
        self.spinner.set_visible(True)
        self.spinner.set_no_show_all(False)
        self.spinner.start()
        self.report_button.remove(self.report_label)
        self.report_button.add(self.spinner)
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def do_icon_uploaded(self, signal):
        if signal:
            try:
                self.desktop_file.report()
            except ThemeNotSupported:
                self.notification.set_message(_("Theme not supported"))
                self.notification.set_type(Gtk.MessageType.INFO)
                self.notification.show()
        self.report_button.remove(self.spinner)
        self.report_button.add(self.report_label)
        self.spinner.set_visible(False)
        self.spinner.set_no_show_all(True)
        self.spinner.stop()
        self.report_button.get_style_context().add_class("text-button")
        self.report_button.set_sensitive(True)
