#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>


from .atlas_api_sdk import Atlas
from .database_user import DatabaseUser


class AtlasProject(object):
    """
    Class to represent a project
    """

    def __init__(self, atlas_manager: Atlas, project_id: str):
        """

        :param Atlas atlas_manager:
        :param str project_id:
        """
        self.project_id = project_id
        self._atlas_manager = atlas_manager
        self.uri = f"{self._atlas_manager.url}/groups/{self.project_id}"

        self._users_uri = f"{self.uri}/databaseUsers"

    @property
    def atlas_manager(self):
        return self._atlas_manager

    @property
    def users(self):
        req = self.atlas_manager.get_raw(self._users_uri)
        _users = {}
        for result in req.json()["results"]:
            _user = DatabaseUser(
                self._atlas_manager,
                self,
                result["username"],
            )
            _user.set_from_api_describe(**result)
            _users[result["username"]] = _user
        return _users
