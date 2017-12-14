from os import path
from tempfile import NamedTemporaryFile
from abc import ABCMeta, abstractmethod
from subprocess import Popen, PIPE


class Upload:
    __metaclass__ = ABCMeta

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @abstractmethod
    def upload_icon(self, icon_path, app_name):
        """Upload the icon."""

    def upload(self, icon_path, app_name=None):
        icon_extension = path.splitext(icon_path)[1].lower().strip(".")
        if icon_extension in ["svg", "png", "xpm"]:
            outfile = NamedTemporaryFile().name
            to_png(icon_path, outfile, 48, 48)
            icon_path = outfile
            return self.upload_icon(icon_path, app_name)
        return None


def to_png(inputfile, outfile, width, height):
    """
        Converts svg/xpm files to png using ImageMagick
        @file_path : String; the svg file absolute path
        @dest_path : String; the png file absolute path
    """
    cmd = Popen([
        "convert", "-background", "none",
        "-resize", "{}x{}".format(str(width), str(height)),
        inputfile, outfile
    ], stdout=PIPE, stdin=PIPE)
    output, error = cmd.communicate()
