# Я.Диск токен y0_AgAAAABXNYkzAADLWwAAAADfYV42nUnKXoX7RL2cTONqacHSVlt3h9g
import requests

from pprint import pprint
from base64 import b64encode


TOKEN = "y0_AgAAAABXNYkzAADLWwAAAADfYV42nUnKXoX7RL2cTONqacHSVlt3h9g"

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def basic_auth(self, username, password):
        token = b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        return href

    def upload_to_ya_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path)
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")




if __name__ == '__main__':
    ya = YaUploader(token=TOKEN)
    ya.upload_to_ya_disk('netology/file_to_YaDisk.txt', 'file_to_YaDisk.txt')
