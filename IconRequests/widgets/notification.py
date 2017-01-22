from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk

class Notification:

	def __init__(self, notification, notification_label):
		self.notification = notification
		self.label = notification_label
		self.notification.connect("response", self.response)

	def set_message(self, message):
		self.label.set_text(message)

	def response(self, *args):
		self.hide()

	def set_type(self, type):
		if not isinstance(type, Gtk.MessageType):
			type = Gtk.MessageType.INFO
		self.notification.set_message_type(type)

	def show(self):
		self.notification.get_parent().set_reveal_child(True)

	def hide(self):
		self.notification.get_parent().set_reveal_child(False)
