#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""Main module."""

import logging as logthings
import sys

import requests
from requests.auth import HTTPDigestAuth

from .errors import evaluate_atlas_api_return


def setup_logging():
    """Function to setup logging for ECS ComposeX.
    In case this is used in a Lambda function, removes the AWS Lambda default log handler

    :returns: the_logger
    :rtype: Logger
    """
    default_level = True
    formats = {
        "INFO": logthings.Formatter(
            "%(asctime)s [%(levelname)8s] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        ),
        "DEBUG": logthings.Formatter(
            "%(asctime)s [%(levelname)8s] %(filename)s.%(lineno)d , %(funcName)s, %(message)s",
            "%Y-%m-%d %H:%M:%S",
        ),
    }

    logthings.basicConfig(level="INFO")
    root_logger = logthings.getLogger()
    for h in root_logger.handlers:
        root_logger.removeHandler(h)
    the_logger = logthings.getLogger("mongodb_atlas_api_sdk")

    if not the_logger.handlers:
        if default_level:
            formatter = formats["INFO"]
        else:
            formatter = formats["DEBUG"]
        handler = logthings.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        the_logger.addHandler(handler)

    return the_logger


LOGGER = setup_logging()


class Atlas(object):
    """
    Main class for all others


    :cvar str _hostname: The MongoDB API Hostname
    :cvar str _api: Path to the API
    :
    """

    _hostname = "cloud.mongodb.com"
    _api = "/api/atlas/v1.0"

    def __init__(
        self,
        public_key: str,
        private_key: str,
        api_path: str = None,
        hostname: str = None,
    ):
        self.public_key = public_key
        self.private_key = private_key
        self.api_path = self._api if api_path is None else api_path
        self.hostname = self._hostname if hostname is None else hostname

        self.url = f"https://{self.hostname}{self.api_path}"
        self.auth = HTTPDigestAuth(self.public_key, self.private_key)
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
        }

    @evaluate_atlas_api_return
    def get_raw(self, url: str = None, ignore_failure: bool = False, **kwargs):
        return requests.get(
            url, auth=self.auth, headers=self.headers, verify=True, **kwargs
        )

    @evaluate_atlas_api_return
    def post_raw(self, url: str = None, **kwargs):
        return requests.post(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=True,
            **kwargs,
        )

    @evaluate_atlas_api_return
    def put_raw(self, url: str = None, **kwargs):

        return requests.put(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=True,
            **kwargs,
        )

    @evaluate_atlas_api_return
    def patch_raw(self, url: str = None, **kwargs):

        return requests.patch(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=True,
            **kwargs,
        )

    @evaluate_atlas_api_return
    def delete_raw(self, url: str = None, **kwargs):
        return requests.delete(
            url, auth=self.auth, headers=self.headers, verify=True, **kwargs
        )
