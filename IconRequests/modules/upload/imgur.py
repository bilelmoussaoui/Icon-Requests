import requests
from IconRequests.modules.settings import Settings
from IconRequests.modules.upload.upload import Upload, ConnexionError
from os import path
from base64 import b64encode

UPLOAD_URI = "https://api.imgur.com/3/upload"

class Imgur(Upload):

    def __init__(self, settings):
        super(Imgur, self).__init__()
        self.client_id = settings.get_imgur_client_id()

    def upload_icon(self, image_path, title=None):
        if path.isfile(image_path):
            with open(image_path, 'rb') as image_obj:
                image_data = b64encode(image_obj.read())
            image_obj.close()

            headers = {
                "Authorization": "Client-ID {0}".format(self.client_id),
                "Accept": "application/json"
            }
            if not title:
                title = path.basename(image_path)

            data = {
                "type": "base64",
                "image": image_data,
                "title": title
            }
            try:
                query = requests.post(UPLOAD_URI, data, headers=headers, timeout=0.05)
                if query.status_code == 200:
                    return query.json()["data"]["link"]
                else:
                    raise ConnexionError
                    return None
            except requests.exceptions.ConnectionError:
                raise ConnexionError
                return None
        else:
            return None
