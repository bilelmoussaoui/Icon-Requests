from gettext import gettext as _
from os import path
from IconRequests.utils import get_icon, copy_file
from threading import Thread
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango


class ApplicationRow(Gtk.ListBoxRow):

    def __init__(self, desktop_file):
        Gtk.ListBoxRow.__init__(self)
        self.desktop_file = desktop_file
        self._build_widgets()
        self.show_all()

    def _build_widgets(self):
        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        info_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Application icon
        image = get_icon(self.desktop_file.icon_path)
        # Application Name
        name = Gtk.Label()
        name.set_ellipsize(Pango.EllipsizeMode.END)
        name.set_halign(Gtk.Align.START)
        name.set_text(self.desktop_file.getName())
        name.get_style_context().add_class("application-name")
        # Application Description
        description = Gtk.Label()
        description.set_halign(Gtk.Align.START)
        description.set_text(self.desktop_file.getComment())
        description.set_tooltip_text(self.desktop_file.getComment())
        description.set_ellipsize(Pango.EllipsizeMode.END)
        description.get_style_context().add_class("application-label")
        # Application destkop file path
        desktop_file = Gtk.Label()
        desktop_file.set_halign(Gtk.Align.START)
        file_path = path.join(self.desktop_file.path,
                              self.desktop_file.desktop_file)
        desktop_file.set_text(file_path)
        desktop_file.set_tooltip_text(file_path)
        desktop_file.set_ellipsize(Pango.EllipsizeMode.END)
        desktop_file.get_style_context().add_class("application-path")

        if (self.desktop_file.is_hardcoded or
                not self.desktop_file.is_supported):
            # Only needed when there's a possible action to be done
            self._spinner = Gtk.Spinner()
            self._spinner.set_visible(False)
            self._spinner.set_no_show_all(True)

            self._report_label = Gtk.Label()
            self._report_label.set_text(_("Report"))
            self._report_button = Gtk.Button()
            self._report_button.add(self._report_label)
            self._report_button.get_style_context().add_class("text-button")
            self._report_button.set_valign(Gtk.Align.CENTER)
            container.pack_end(self._report_button, False, False, 6)

            if self.desktop_file.is_hardcoded:
                self._report_button.connect("clicked",
                                            self._report_hardcoded_icon)
            else:
                self._report_button.connect("clicked",
                                            self._report_missing_icon)

        info_container.pack_start(name, False, False, 3)
        info_container.pack_start(description, False, False, 3)
        info_container.pack_start(desktop_file, False, False, 3)

        container.pack_start(image, False, False, 6)
        container.pack_start(info_container, False, False, 6)
        self.add(container)

    def _report_missing_icon(self, *args):
        self._do_action_started()

        def report_missing_icon():
            upload_status = self.desktop_file.upload()
            if upload_status:
                self.desktop_file.report()
            self._do_action_finished()
        # Start the thread!
        thread = Thread(target=report_missing_icon)
        thread.daemon = True
        thread.start()

    def _report_hardcoded_icon(self, *args):
        """Report hardcoded icon to hardcode-fixer repository."""
        self._do_action_started()

        def report_hardcoded_icon():
            self.desktop_file.report_hardcoded()
            self._do_action_finished()
        # Start the thread!
        thread = Thread(target=report_hardcoded_icon)
        thread.daemon = True
        thread.start()

    def _do_action_started(self):
        """Widgets modification whenever an action starts."""
        # Refactor the report button
        self._report_button.set_sensitive(False)
        self._report_button.get_style_context().remove_class("text-button")
        self._report_button.remove(self._report_label)
        self._report_button.add(self._spinner)
        # Show the spinner inside the button & start it
        self._spinner.set_visible(True)
        self._spinner.set_no_show_all(False)
        self._spinner.start()

    def _do_action_finished(self):
        """Widgets modification once an action is finished."""
        # Stop & Hide the spinner
        self._spinner.set_visible(False)
        self._spinner.set_no_show_all(True)
        self._spinner.stop()
        # Remove the spinner from the report button
        self._report_button.remove(self._spinner)
        self._report_button.add(self._report_label)
        self._report_button.get_style_context().add_class("text-button")
        self._report_button.set_sensitive(True)

    def get_search_data(self):
        """Used by SearchBar to filter Rows."""
        return self.desktop_file.getName()
