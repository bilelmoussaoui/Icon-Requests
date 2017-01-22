from os import path
from IconRequests.utils import convert_svg2png
from tempfile import NamedTemporaryFile
from PIL import Image

class Upload:

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id


    def upload(self, icon_path, app_name=None):
        icon_extension = path.splitext(icon_path)[1].lower().strip(".")
        was_scaled = False
        if icon_extension in ["svg", "png"]:
            outfile = NamedTemporaryFile().name
            if icon_extension == "svg":
                convert_svg2png(icon_path, outfile, 48, 48)
                icon_path = outfile
                was_scaled = True
                icon_extension = "png"
            if icon_extension == "png":
                if not was_scaled:
                    img = Image.open(icon_path)
                    img = img.resize((48, 48), Image.ANTIALIAS)
                    img.save(outfile, "PNG")
                    icon_path = outfile
                icon_url = self.upload_icon(icon_path, app_name)
                return icon_url
        return None

class ConnexionError(Exception):
    def __init__(self):
        super(ConnexionError, self).__init__()