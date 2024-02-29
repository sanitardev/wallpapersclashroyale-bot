import io
from config import API_URL
import requests
import urllib3
from aiogram import types

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class API:
    def __init__(self):
        self.random_url = API_URL + "random"
        self.all_url = API_URL + "getAll"
        self.add_url = API_URL + "addImage"
        self.delete_url = API_URL + "deleteImage"

    def get_random_url(self):
        response = requests.get(self.random_url, verify=False)
        if response.status_code == 200:
            return response.text,{response.status_code}
        else: 
            return None, {response.status_code}

    def get_wallpaper_by_url(self, url):
        image_response = requests.get(url, verify=False)
        if image_response.status_code == 200:
            image_bytes = image_response.content
            photo = types.InputFile(io.BytesIO(image_bytes), filename='wallpaper.jpg')
            return photo, {image_response.status_code}
        else:
             return None, {image_response.status_code}

    def get_all_urls(self):
        response = requests.get(self.all_url, verify=False)
        if response.status_code == 200:
            return response.text
        else: 
            return f"Ошибка {response.status_code}!"

    def add_wallpaper_by_url(self, url):
        headers = {"Content-Type": "application/json"}
        payload = {"imageUrl": url}
        response = requests.post(self.add_url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "code": response.status_code}

    def delete_wallpaper(self, file):
        response = requests.delete(self.delete_url + f"/{file}", verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "code": response.status_code}