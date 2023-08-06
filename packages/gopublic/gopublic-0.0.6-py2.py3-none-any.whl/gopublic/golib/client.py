from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import json

from future import standard_library

from gopublic.golib.exceptions import GopublishApiError, GopublishConnectionError, GopublishNotImplementedError, GopublishParameterError

import requests

standard_library.install_aliases()


class Client(object):
    """
    Base client class implementing methods to make queries to the server
    """

    def __init__(self, url, endpoints, gopublish_mode, auth):
        self.url = url
        self.endpoints = endpoints
        self.gopublish_mode = gopublish_mode
        self.auth = auth

    def _api_call(self, call_type, endpoint_name, body={}, headers=None):

        url, body = self._format_url(call_type, endpoint_name, body)

        try:
            if call_type == "get":
                r = requests.get(url, params=body, headers=headers, auth=self.auth)
            elif call_type == "delete":
                r = requests.delete(url, params=body, headers=headers, auth=self.auth)
            elif call_type == "post":
                r = requests.post(url, json=body, headers=headers, auth=self.auth)
            elif call_type == "put":
                r = requests.put(url, json=body, headers=headers, auth=self.auth)

            if 400 <= r.status_code <= 499:
                try:
                    data = r.json()
                    raise GopublishApiError("API call returned the following error: '{}'".format(data.get('error', "")))
                except json.decoder.JSONDecodeError:
                    raise GopublishApiError("API call returned the following error code: '{}'".format(r.status_code))
            elif r.status_code == 502:
                raise GopublishApiError("Unknown server error")
            else:
                return r.json()

        except requests.exceptions.RequestException:
            raise GopublishConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))

    def _format_url(self, call_type, endpoint_name, body):

        endpoint = self.endpoints.get(endpoint_name)
        if not endpoint:
            raise GopublishNotImplementedError()

        # Fill parameters in the url
        groups = re.findall(r'<(.*?)>', endpoint)
        for group in groups:
            if group not in body:
                raise GopublishApiError("Missing get parameter " + group)
            endpoint = endpoint.replace("<{}>".format(group), body.get(group))
            body.pop(group)

        return "{}{}".format(self.url, endpoint), body

    def _parse_input_values(self, val, val_name):
        if not val:
            return []
        if isinstance(val, list):
            return val
        elif isinstance(val, str):
            return [data.strip() for data in val.split(",")]
        else:
            raise GopublishParameterError("{} must either be a list or a comma-separated string".format(val_name))
