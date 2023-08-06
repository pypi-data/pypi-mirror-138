from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from future import standard_library

from gopublic.golib.client import Client
from gopublic.golib.exceptions import GopublishTokenMissingError, GopublishParameterError

standard_library.install_aliases()


class FileClient(Client):
    """
    Manipulate files managed by Gopublish
    """

    def list(self, tags="", limit=None, offset=None):
        """
        List files published in Gopublish

        :type tags: str
        :param tags: Comma-separated tags

        :type limit: int
        :param limit: Limit the results numbers

        :type offset: int
        :param offset: Offset for listing the results (used with limit)

        :rtype: dict
        :return: Dict with files and total count
        """

        body = {}

        tags = self._parse_input_values(tags, "Tags")
        if tags:
            body['tags'] = tags

        if offset and not limit:
            offset = None
        if limit:
            body['limit'] = limit
        if offset:
            body['offset'] = offset

        return self._api_call("get", "list_files", body)

    def search(self, query="", tags="", limit=None, offset=None):
        """
        Launch a pull task

        :type query: str
        :param query: Either a search term, or a file UID

        :type tags: str
        :param tags: Comma-separated tags

        :type limit: int
        :param limit: Limit the results numbers

        :type offset: int
        :param offset: Offset for listing the results (used with limit)

        :rtype: dict
        :return: Dict with files and total count
        """
        body = {}

        if query:
            body['file'] = query

        tags = self._parse_input_values(tags, "Tags")

        if offset and not limit:
            offset = None
        if limit:
            body['limit'] = limit
        if offset:
            body['offset'] = offset

        if tags:
            body['tags'] = tags

        return self._api_call("get", "search", body)

    def publish(self, path, tags="", linked_to="", contact="", email="", token="", inherit_tags=True):
        """
        Launch a publish task

        :type path: str
        :param path: Path to the file to be published

        :type tags: str
        :param tags: Comma-separated tags

        :type linked_to: str
        :param linked_to: id of the original file this file is a version of

        :type contact: str
        :param contact: Contact email for this file

        :type email: str
        :param email: Contact email for notification when publication is done

        :type token: str
        :param token: Your Gopublish token.

        :type inherit_tags: bool
        :param inherit_tags: Inherit linked file tags. Default to True

        :rtype: dict
        :return: Dictionnary containing the response
        """

        body = {"path": path}
        if email:
            body['email'] = email

        if contact:
            body['contact'] = contact

        tags = self._parse_input_values(tags, "Tags")
        if tags:
            body['tags'] = tags

        if linked_to:
            body['linked_to'] = linked_to

        body['inherit_tags'] = inherit_tags

        if not token:
            if os.getenv("GOPUBLISH_TOKEN"):
                token = os.getenv("GOPUBLISH_TOKEN")
            else:
                raise GopublishTokenMissingError("Missing token: either specify it with --token, or set it as GOPUBLISH_TOKEN in your environnment")
        headers = {"X-Auth-Token": "Bearer " + token}

        return self._api_call("post", "publish_file", body, headers=headers)

    def tag(self, file_id, tags="", token=""):
        """
        Add one or more tags to a file

        :type file_id: str
        :param file_id: File id

        :type tags: str
        :param tags: Comma-separated tags to add

        :type token: str
        :param token: Your Gopublish token.

        :rtype: dict
        :return: Dict with file state
        """

        body = {'file_id': file_id}

        tags = self._parse_input_values(tags, "Tags")
        if not tags:
            raise GopublishParameterError("Please provide at least one tag to add")
        body['tags'] = tags

        if not token:
            if os.getenv("GOPUBLISH_TOKEN"):
                token = os.getenv("GOPUBLISH_TOKEN")
            else:
                raise GopublishTokenMissingError("Missing token: either specify it with --token, or set it as GOPUBLISH_TOKEN in your environnment")
        headers = {"X-Auth-Token": "Bearer " + token}

        return self._api_call("put", "tag_file", body, headers=headers)

    def untag(self, file_id, tags="", token=""):
        """
        Remove one or more tag from a file

        :type file_id: str
        :param file_id: File id

        :type tags: str
        :param tags: Comma-separated tags to add

        :type token: str
        :param token: Your Gopublish token.

        :rtype: dict
        :return: Dict with file state
        """

        body = {'file_id': file_id}

        tags = self._parse_input_values(tags, "Tags")
        if not tags:
            raise GopublishParameterError("Please provide at least one tag to add")
        body['tags'] = tags

        if not token:
            if os.getenv("GOPUBLISH_TOKEN"):
                token = os.getenv("GOPUBLISH_TOKEN")
            else:
                raise GopublishTokenMissingError("Missing token: either specify it with --token, or set it as GOPUBLISH_TOKEN in your environnment")
        headers = {"X-Auth-Token": "Bearer " + token}

        return self._api_call("put", "untag_file", body, headers=headers)

    def unpublish(self, file_id, token=""):
        """
        Unpublish a file

        :type file_id: str
        :param file_id: File id

        :type token: str
        :param token: Your Gopublish token.

        :rtype: dict
        :return: Dictionnary containing the response
        """

        body = {'file_id': file_id}

        if not token:
            if os.getenv("GOPUBLISH_TOKEN"):
                token = os.getenv("GOPUBLISH_TOKEN")
            else:
                raise GopublishTokenMissingError("Missing token: either specify it with --token, or set it as GOPUBLISH_TOKEN in your environnment")
        headers = {"X-Auth-Token": "Bearer " + token}

        return self._api_call("delete", "unpublish_file", body=body, headers=headers)

    def delete(self, file_id, token=""):
        """
        Delete a file (admin_restricted)

        :type file_id: str
        :param file_id: File id

        :type token: str
        :param token: Your Gopublish token.

        :rtype: dict
        :return: Dictionnary containing the response
        """

        body = {'file_id': file_id}

        if not token:
            if os.getenv("GOPUBLISH_TOKEN"):
                token = os.getenv("GOPUBLISH_TOKEN")
            else:
                raise GopublishTokenMissingError("Missing token: either specify it with --token, or set it as GOPUBLISH_TOKEN in your environnment")
        headers = {"X-Auth-Token": "Bearer " + token}

        return self._api_call("delete", "delete_file", body=body, headers=headers)
