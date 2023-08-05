#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

"""
DatabaseUser management class
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

import requests
from compose_x_common.compose_x_common import keyisset, set_else_none

from .atlas_api_sdk import Atlas, setup_logging

if TYPE_CHECKING:
    from .atlas_project import AtlasProject

LOGGER = setup_logging()


class DatabaseUser(object):
    """
    Class to represent and manipulate the Database User
    """

    AWS_TYPES = ["ROLE", "USER"]

    def __init__(
        self,
        atlas_manager: Atlas,
        atlas_project: AtlasProject,
        username: str,
        password: str = None,
        database: str = None,
        aws_iam_type: str = None,
        ldap_auth_type: str = None,
        x509_type: str = None,
    ) -> None:
        """
        :param atlas_project:
        :param username:
        :param database:
        """
        self._atlas_manager = atlas_manager
        self._atlas_project = atlas_project
        self._username = username
        self._links = []
        self._roles = []
        self._scopes = []
        self._aws_iam_type = aws_iam_type
        self._ldap_auth_type = ldap_auth_type
        self._x509_type = x509_type
        self._password = password

        if database:
            self._database = database
        else:
            self._database = "admin"

        self.set_id_properties()

    def set_id_properties(self):
        """
        Enforces that if one setting for Auth is set, all others are voided
        """
        if self._aws_iam_type in self.AWS_TYPES or self._username.startswith(
            "arn:aws:iam::"
        ):
            self._database = r"$external"
            if self._aws_iam_type is None:
                self.define_aws_iam_type()
            self._ldap_auth_type = None
            self._x509_type = None
            self._password = None

        elif self._password and self._password != "NONE":
            self._ldap_auth_type = None
            self._x509_type = None
            self._aws_iam_type = None

        elif self._x509_type and self._x509_type != "NONE":
            self._database = r"$external"
            self._password = None
            self._ldap_auth_type = None
            self._aws_iam_type = None

        elif self._ldap_auth_type and self._ldap_auth_type != "NONE":
            self._database = r"$external"
            self._password = None
            self._x509_type = None
            self._aws_iam_type = None

    def __repr__(self):
        return f"{self.group_id}::{self._username}@{self._database}"

    def define_aws_iam_type(self):
        """
        Simple function to define the awsIAMType of the resource if the username looks like an AWS ARN but
        the aws_iam_type was not set
        """
        arn_valid = re.compile(
            r"^arn:aws(?:-[a-z-]+)?:iam::[0-9]{12}:(?P<type>role|user)/[\S]+$"
        )
        parts = arn_valid.match(self._username)
        if not parts:
            raise ValueError(
                "ARN",
                self._username,
                "is not a valid ARN for a user or a role. Must match",
                arn_valid.pattern,
            )
        self._aws_iam_type = parts.group("type").upper()

    def set_from_api_describe(self, **kwargs):
        """
        Sets the attributes values based on the GET reply from MongoDB API.
        """
        self._links = set_else_none("links", kwargs, [])
        self._username = kwargs["username"]
        self._database = kwargs["databaseName"]
        self._aws_iam_type = set_else_none("awsIAMType", kwargs, "NONE")
        self._x509_type = set_else_none("x509Type", kwargs, "NONE")
        self._ldap_auth_type = set_else_none("ldapAuthType", kwargs, "NONE")
        if keyisset("roles", kwargs):
            for _role in kwargs["roles"]:
                self.add_role(**_role)
        if keyisset("scopes", kwargs):
            for _scope in kwargs["scopes"]:
                self.add_scope(**_scope)
        self.set_id_properties()

    @property
    def group_id(self):
        return self._atlas_project.project_id

    @property
    def username(self):
        return self._username

    @property
    def roles(self):
        return self._roles

    @property
    def scopes(self):
        return self._scopes

    @property
    def href(self):
        for link in self._links:
            if "href" in link and "rel" in link and link["rel"] == "self":
                return link["href"]
        return None

    @property
    def uri(self):
        if self.href:
            return self.href
        else:
            if self._aws_iam_type in self.AWS_TYPES:
                return (
                    f"{self._atlas_project.uri}/databaseUsers/{self._database}/"
                    f"{requests.utils.quote(self._username, safe='')}"
                )
            else:
                return f"{self._atlas_project.uri}/databaseUsers/{self._database}/{self._username}"

    @property
    def exists(self):
        """
        Whether the user exists in the project

        :rtype: bool
        """
        _req = self._atlas_manager.get_raw(self.uri, ignore_failure=True)
        if _req.status_code == 404:
            return False
        return True

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, secret):
        self._password = secret

    @property
    def model(self):
        self.set_id_properties()
        content = {
            "databaseName": self._database,
            "roles": [
                role.model for role in self.roles if isinstance(role, DatabaseUserRole)
            ],
            "scopes": [
                scope.model
                for scope in self.scopes
                if isinstance(scope, DatabaseUserScope)
            ],
            "username": self._username,
        }
        if self.password:
            content["password"] = self._password
        elif self._ldap_auth_type:
            content["ldapAuthType"] = self._ldap_auth_type
        elif self._x509_type:
            content["x509Type"] = self._x509_type
        elif self._aws_iam_type:
            content["awsIAMType"] = self._aws_iam_type
        return content

    def create(self):
        """
        To create a new user
        """
        req = self._atlas_manager.post_raw(
            self._atlas_project._users_uri, json=self.model
        )
        self.set_from_api_describe(**req.json())
        LOGGER.debug(f"{self} - Created successfully.")

    def read(self):
        _req = self._atlas_manager.get_raw(self.uri)
        return _req.json()

    def update(self):
        if not self.href and self.exists:
            self.set_from_api_describe(**self.read())
        _req = self._atlas_manager.patch_raw(self.uri, json=self.model)
        self.set_from_api_describe(**_req.json())
        LOGGER.debug(f"{self} - Updated successfully")

    def delete(self):
        """
        To delete one self from project
        """
        if not self.href and self.exists:
            self.set_from_api_describe(**self.read())
        _req = self._atlas_manager.delete_raw(self.uri)
        if _req.status_code == 204:
            LOGGER.debug(f"{self} - Deleted successfully")
            self._roles = []
            self._scopes = []
        else:
            LOGGER.error(f"{_req.status_code} - Error on delete for {self}")

    def add_role(
        self, name: str = None, database: str = None, collection: str = None, **kwargs
    ):
        """
        Adds a new DatabaseUserRole to user
        """
        role_name = name if name else set_else_none("roleName", kwargs)
        role_database = database if database else set_else_none("databaseName", kwargs)
        role_collection = (
            collection if collection else set_else_none("collectionName", kwargs)
        )
        if not role_database and role_name == "readWriteAnyDatabase":
            role_database = "admin"
        if not role_name or not role_database:
            raise AttributeError(
                "No roleName nor databaseName set for new DatabaseUserRole",
                role_name,
                role_database,
                role_collection,
                kwargs,
            )
        role = DatabaseUserRole(role_name, role_database, role_collection)
        if role not in self.roles:
            self.roles.append(role)

    def add_scope(self, name: str = None, scope_type: str = None, **kwargs):
        """
        Adds a new DatabaseUserRole to user
        """
        _scope_name = name if name else set_else_none("name", kwargs)
        _scope_type = scope_type if scope_type else set_else_none("type", kwargs)
        if not _scope_name or not _scope_type:
            raise AttributeError(
                "Missing scope name or scope type for DatabaseUserScope",
                _scope_name,
                _scope_type,
                kwargs,
            )
        scope = DatabaseUserScope(_scope_name, _scope_type)
        if scope not in self.scopes:
            self.scopes.append(scope)


class DatabaseUserRole(object):
    """
    Represents a DB User role
    """

    admin_only_roles = [
        "atlasAdmin" "backup",
        "clusterMonitor",
        "readWriteAnyDatabase",
        "readAnyDatabase",
        "killOpSession",
        "enableSharding",
        "dbAdminAnyDatabase",
    ]
    non_admin_roles = ["read", "readWrite", "dbAdmin"]
    collections_only_roles = ["read", "readWrite"]
    predefined_roles = admin_only_roles + non_admin_roles

    def __init__(self, name: str, database: str = None, collection: str = None):
        if (
            name in self.non_admin_roles
            and collection
            and name not in self.collections_only_roles
        ):
            raise ValueError(
                f"Predefined role {name} is not valid for collections. Use one of",
                self.collections_only_roles,
                "or a custom role",
            )
        self.database = database
        self.role_name = name
        self.collection = collection

        if self.role_name in self.admin_only_roles:
            self.database = "admin"
            self.collection = None

    @property
    def model(self):
        """
        Returns dict that is used for API calls related to the user
        """
        content = {"databaseName": self.database, "roleName": self.role_name}
        if self.collection:
            content["collectionName"] = self.collection
        return content

    def __eq__(self, other):
        if other.database == self.database and other.role_name == self.role_name:
            return True
        return False


class DatabaseUserScope(object):
    """
    Represents a database user scope
    """

    allowed_scopes = ["CLUSTER", "DATA_LAKE"]

    def __init__(self, scope_name: str, scope_type: str):
        if scope_type not in self.allowed_scopes:
            raise ValueError(
                "scope_type must be one of", self.allowed_scopes, "got", scope_type
            )
        self.name = scope_name
        self.type = scope_type

    def __eq__(self, other):
        if self.name == other.name and self.type == other.type:
            return True
        return False

    def __repr__(self):
        return f"{self.type}::{self.name}"

    @property
    def model(self):
        """
        Returns dict for user API interactions
        """
        content = {"name": self.name, "type": self.type}
        return content
