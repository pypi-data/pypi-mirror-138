#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>


from __future__ import annotations

import ipaddress
from os import environ
from typing import TYPE_CHECKING

import awsipranges
import requests
from compose_x_common.compose_x_common import keyisset, set_else_none

from .atlas_api_sdk import Atlas

if TYPE_CHECKING:
    from .atlas_project import AtlasProject


def set_ip_network(ip_address):
    """
    Returns ipaddress.IPv4Network to use next

    :param ip_address:
    :rtype: ipaddress.IPv4Network
    """
    if isinstance(ipaddress, ipaddress.IPv4Network):
        return ip_address
    else:
        return ipaddress.IPv4Network(ip_address)


class ApiKey(object):
    """
    Class to represent an API Key
    """

    hostname = "cloud.mongodb.com"
    api_path = "/api/atlas/v1.0"
    base_url = f"https://{hostname}{api_path}"

    def __init__(
        self,
        atlas: Atlas,
        org_id: str,
        key_id: str = None,
        public_id: str = None,
        key_secret: str = None,
    ):
        """
        Sets an API Key up

        :param atlas:
        :param key_id:
        :param key_secret:
        """
        self._atlas_manager = atlas
        self._org_id = org_id
        self._links = []
        self._ip_access_list = []
        self._public_id = public_id
        self._secret = key_secret
        self._roles = []
        self._href = None
        self._id = key_id
        if public_id and not key_id:
            self.set_key_from_org_keys(public_id)
        elif key_id and not public_id:
            self.href = f"{self.base_url}/orgs/{org_id}/apiKeys/{key_id}"
        elif public_id and key_id:
            self.set_key_from_org_keys(public_id)
        else:
            raise AttributeError(
                "You must specify at least one of", ["key_id", "public_id"]
            )

    @property
    def href(self):
        if self._href:
            return self._href
        for link in self._links:
            if "href" in link and "rel" in link and link["rel"] == "self":
                return link["href"]
        return None

    @href.setter
    def href(self, links: list = None):
        if not links and not self._links and self._public_id:
            self.set_key_from_org_keys(self._public_id)
        for link in self._links:
            if "href" in link and "rel" in link and link["rel"] == "self":
                self._href = link["href"]

    @property
    def exists(self):
        """
        Whether the user exists in the project

        :rtype: bool
        """
        if not self.href:
            return False
        _req = self._atlas_manager.get_raw(self.href, ignore_failure=True)
        if _req.status_code == 404:
            return False
        return True

    @property
    def access_list(self):
        """
        List of all the IP / CIDR Block currently authorized

        :rtype: list
        """
        return self.get_all_access_list()["results"]

    def set_key_from_org_keys(self, public_id: str):
        """
        Function helper that queries the organization keys and matches to the key based on the publicKey value.

        :param str public_id:
        :return:
        """
        _req = self._atlas_manager.get_raw(
            f"{self.base_url}/orgs/{self._org_id}/apiKeys"
        )
        for key in _req.json()["results"]:
            if key["publicKey"] == public_id:
                self._links = key["links"]
                self._id = key["id"]
                self._roles = keyisset("roles", key)
        if not self._id and not self._href:
            raise LookupError(
                f"Failed to set the href and properties with public_key {public_id}"
            )

    def get_all_access_list(self):
        if not self.href and self._public_id:
            self.href = self._public_id
        url = f"{self.href}/accessList"
        _req = self._atlas_manager.get_raw(url)
        return _req.json()

    def add_ip_address(self, ip_address):
        """
        Updates the key properties
        """
        _ip = set_ip_network(ip_address)
        if _ip._prefixlen == 32:
            self._atlas_manager.post_raw(
                f"{self.href}/accessList",
                json=[{"ipAddress": str(_ip.network_address)}],
            )
        else:
            self._atlas_manager.post_raw(
                f"{self.href}/accessList", json=[{"cidrBlock": _ip.exploded}]
            )

    def bulk_add_ip_address_blocks(self, ip_addresses: list):
        """
        Creates a bulk list of IP addresses to add to ACL

        :param list ip_addresses:
        """
        to_add = []
        for ip_address in ip_addresses:
            _ip = set_ip_network(ip_address)
            to_add.append({"cidrBlock": _ip.exploded})
        self._atlas_manager.post_raw(f"{self.href}/accessList", json=to_add)

    def delete_ip_address(self, ip_address):
        _ip = set_ip_network(ip_address)
        self._atlas_manager.delete_raw(
            f"{self.href}/accessList/{requests.utils.quote(_ip.exploded, safe='')}"
        )

    def add_aws_ip_ranges(self, region: str = None, services: str = None):
        """
        Function to automatically add the AWS IP Ranges to a key.
        It will verify that the block is not already set before adding to the list.

        :param str region:
        :param str services:
        """
        if not region and not environ.get(
            "AWS_DEFAULT_REGION", environ.get("AWS_REGION", None)
        ):
            raise KeyError(
                "You must specify the region or set AWS_DEFAULT_REGION or AWS_REGION"
            )
        if not services:
            services = "EC2"
        aws_ip_ranges = awsipranges.get_ranges()
        region_ranges = aws_ip_ranges.filter(
            services=services, regions=region, versions=4
        )
        _current_ip_blocks = [
            ipaddress.IPv4Network(
                set_else_none(
                    "cidrBlock",
                    _mongo_ip,
                    alt_value=set_else_none("ipAddress", _mongo_ip),
                )
            )
            for _mongo_ip in self.access_list
        ]
        to_add = []
        for _aws_ip_range in region_ranges:
            if _aws_ip_range in _current_ip_blocks:
                continue
            to_add.append(_aws_ip_range)
        self.bulk_add_ip_address_blocks(to_add)
