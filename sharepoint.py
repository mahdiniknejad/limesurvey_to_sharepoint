import os
import json
from shareplum import Site, Office365
from shareplum.site import Version


class SharePoint:

    def __init__(self, url, username, password, site, doc, dir):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__site = site
        self.__doc = doc
        self.dir = dir

        self.authcookie = Office365(
            self.__url,
            username=self.__username,
            password=self.__password
        ).GetCookies()

        self.site = Site(
            self.__site,
            version=Version.v365,
            authcookie=self.authcookie
        )

    def connect_folder(self, folder_name):
        sharepoint_dir = '\\'.join([self.__doc, folder_name])
        self.folder = self.site.Folder(sharepoint_dir)

        return self.folder

    def download_file(self, download_path, file_name, dir):
        self.connect_folder(dir)

        file = self.folder.get_file(file_name)
        with open(download_path + file_name, mode='wb') as f:
            f.write(file)

    def upload_file(self, path, file_name, dir, name):
        self.connect_folder(dir)
        
        with open(path + '/' + file_name, mode='rb') as file:
            file_content = file.read()
        
        self.folder.upload_file(file_content, name)

    def delete_file(self, file_name, dir):
        self.connect_folder(dir)
        self.folder.delete_file(file_name)

    def files_list(self, dir):
        self._folder = self.connect_folder(dir)
        return list(map(lambda obj: obj['Name'], self._folder.files))
