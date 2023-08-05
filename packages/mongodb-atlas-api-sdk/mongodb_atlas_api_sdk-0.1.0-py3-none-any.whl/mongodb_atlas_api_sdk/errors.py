#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

"""
MongoDB Atlas API SDK Exceptions and error handling
"""

from compose_x_common.compose_x_common import keyisset


class AtlasGenericException(Exception):
    """
    Generic class handling for the SDK using the request as input
    """

    def __init__(self, msg, code, details):
        """

        :param msg:
        :param code:
        :param details:
        """
        super().__init__(msg, code, details)
        self.code = code
        self.details = details


class GenericNotFound(AtlasGenericException):
    """
    Generic option for 404 return code
    """

    def __init__(self, code, details):
        super().__init__(details.get("detail", "Resource not found"), code, details)


class GenericUnauthorized(AtlasGenericException):
    """
    Generic option for 401 return code
    """

    def __init__(self, code, details):
        super().__init__(details.get("detail", "Access unauthorized"), code, details)


class GenericForbidden(AtlasGenericException):
    """
    Generic exception for a 403
    """

    def __init__(self, code, details):
        super().__init__(details.get("detail", "403 Forbidden"), code, details)


class DatabaseUserNotFound(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User does not exist"), code, details)


class DatabaseUserConflict(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User already exists"), code, details)


class DatabaseUserInvalidAttribute(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User attribute invalid"), code, details)


class DatabaseUserMissingAttribute(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User attribute missing"), code, details)


class DatabaseUserDuplicateDatabaseRole(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(
            details.get("detail", "Duplicated user roles for database"), code, details
        )


class IpAddressNotOnAccessList(AtlasGenericException):
    """
    Handles IP_ADDRESS_NOT_ON_ACCESS_LIST
    """

    def __init__(self, code, details):
        super().__init__(
            details.get("detail", "IP Address not in ACL"),
            code,
            details,
        )


class ApiKeyIpAddressAlreadyInAccessList(AtlasGenericException):
    """
    Handles ALREADY_IN_ACCESS_LIST
    """

    def __init__(self, code, details):
        super().__init__(details.get("detail", "IP is already ACL"), code, details)


class ApiKeyIpAddressNotInAccessList(AtlasGenericException):
    """
    Handles ALREADY_IN_ACCESS_LIST
    """

    def __init__(self, code, details):
        super().__init__(details.get("detail", "ACL IP not in ACL"), code, details)


class MongoDbAtlasApiException(AtlasGenericException):
    """
    Top class for DatabaseUser exceptions
    """

    MANAGED_ERRORS = {
        "USER_ALREADY_EXISTS": DatabaseUserNotFound,
        "INVALID_ATTRIBUTE": DatabaseUserInvalidAttribute,
        "DUPLICATE_DATABASE_ROLES": DatabaseUserDuplicateDatabaseRole,
        "MISSING_ATTRIBUTE": DatabaseUserMissingAttribute,
        "USER_NOT_FOUND": DatabaseUserNotFound,
        "IP_ADDRESS_NOT_ON_ACCESS_LIST": IpAddressNotOnAccessList,
        "ADDRESS_ALREADY_IN_ACCESS_LIST": ApiKeyIpAddressAlreadyInAccessList,
        "API_KEY_ACCESS_LIST_ENTRY_NOT_FOUND": ApiKeyIpAddressNotInAccessList,
    }

    def __init__(self, code, details):
        if details.get("errorCode", None) in self.MANAGED_ERRORS.keys():
            raise self.MANAGED_ERRORS[details.get("errorCode")](code, details)
        elif code == 404:
            raise GenericNotFound(code, details)
        elif code == 401:
            raise GenericUnauthorized(code, details)
        elif code == 403:
            raise GenericForbidden(code, details)
        super().__init__("Something was wrong with the client request.", code, details)


def evaluate_atlas_api_return(function):
    """
    Decorator to evaluate the requests payload returned
    """

    def wrapped_answer(*args, **kwargs):
        """
        Decorator wrapper
        """
        payload = function(*args, **kwargs)
        if payload.status_code not in [200, 201, 202, 204] and not keyisset(
            "ignore_failure", kwargs
        ):
            details = payload.json()
            raise MongoDbAtlasApiException(payload.status_code, details)

        elif keyisset("ignore_failure", kwargs):
            return payload
        return payload

    return wrapped_answer
