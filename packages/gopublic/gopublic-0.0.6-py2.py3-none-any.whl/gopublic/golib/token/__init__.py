from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import getpass

from future import standard_library

from gopublic.golib.client import Client
from gopublic.golib.exceptions import GopublishParameterError

standard_library.install_aliases()


class TokenClient(Client):
    """
    Manipulate files managed by Gopublish
    """

    def create(self, username, password="", api_key=""):
        """
        Get token

        :type username: str
        :param username: Username

        :type password: str
        :param password: Optional password for library compatibility

        :type api_key: str
        :param api_key: Admin api key

        :rtype: dict
        :return: Dictionnary containg the token
        """

        body = {"username": username}

        if self.gopublish_mode == "prod":
            if api_key:
                body['api_key'] = api_key
            elif not password:
                try:
                    body["password"] = getpass.getpass(prompt='Enter your GenOuest password ')
                except Exception as e:
                    raise GopublishParameterError(str(e))
        else:
            body["password"] = username

        return self._api_call("post", "create_token", body)
