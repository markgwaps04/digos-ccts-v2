from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class AuthenticationFailed(APIException):
    status_code = 501
    default_detail = 'Invalid credentials, Account not found'
    default_code = 'authentication_failed'

class BuildingOwnerNotFound(APIException):
    status_code = 502
    default_detail = 'Could not retrieve information about this user or the user is not a building owner'
    default_code = 'building_owner_not_found'


class ParametersNotValid(APIException):
    status_code = 503
    default_detail = 'Required parameters not satisfy'
    default_code = 'paramters_not_valid'


class InnerException(APIException):
    status_code = 504
    default_detail = 'Inner Error occured while attempting to execute the request'
    default_code = 'inner_exception'


class AccountNotVerified(APIException):
    status_code = 505
    default_detail = 'The Account is not verified'
    default_code = 'account_not_verified'
