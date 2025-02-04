import requests

# from django.core.files import File
# from .models import Profile
from decouple import config
import os


download_path = config("DOWNLOAD_PATH")
if not os.path.exists(download_path):
    os.makedirs(download_path)


def download_image(img_url, download_path=download_path):
    response = requests.get(img_url)
    with open(f"{download_path}/image1.jpg", "wb") as file:
        file.write(response.content)
    return download_path
