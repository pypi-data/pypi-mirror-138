from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

from gopublic.golib.exceptions import GopublishConnectionError
from gopublic.golib.file import FileClient
from gopublic.golib.token import TokenClient

import requests

standard_library.install_aliases()


class GopublishInstance(object):

    def __init__(self, url="http://localhost:80", proxy_username="", proxy_password="", **kwargs):

        url = url.rstrip().rstrip("/")
        self.url = url

        if proxy_username and proxy_password:
            self.auth = (proxy_username, proxy_password)
        else:
            self.auth = None

        self.gopublish_version, self.gopublish_mode = self._get_status()

        self.endpoints = self._get_endpoints()

        # Initialize Clients
        args = (self.url, self.endpoints, self.gopublish_mode, self.auth)
        self.file = FileClient(*args)
        self.token = TokenClient(*args)

    def __str__(self):
        return '<GopublishInstance at {}>'.format(self.url)

    def _get_status(self):

        try:
            r = requests.get("{}/api/status".format(self.url), auth=self.auth)
            if not r.status_code == 200:
                raise requests.exceptions.RequestException
            return (r.json()["version"], r.json()["mode"])
        except requests.exceptions.RequestException:
            raise GopublishConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))

    def _get_endpoints(self):

        try:
            r = requests.get("{}/api/endpoints".format(self.url), auth=self.auth)
            if not r.status_code == 200:
                raise requests.exceptions.RequestException
            return r.json()
        except requests.exceptions.RequestException:
            raise GopublishConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))


__version__ = '0.0.6'

PROJECT_NAME = "gopublic"
