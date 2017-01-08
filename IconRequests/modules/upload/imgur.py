import pyimgur
CLIENT_ID = "01fb07fcc6cc0fe"
CLIENT_SECRET = "3b07f34ec00a9840cde6f6c2e2030138e3f9d430"

def imgur_upload_img(file_path, icon_name):
    img = pyimgur.Imgur(CLIENT_ID)
    uploaded_img = img.upload_image(file_path, title=icon_name)
    return uploaded_img.link
