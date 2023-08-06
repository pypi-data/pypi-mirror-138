import json


class Error(Exception):
    pass


class AuthorizationError(Error):
    def __init__(self, msg):
        super(AuthorizationError, self).__init__(msg)


class ApiError(Error):
    def __init__(self, request):
        try:
            data = request.json()
            error_attributes = ' '.join(['{}: {}'.format(k, v) for k, v in data.items()])
        except json.decoder.JSONDecodeError:
            error_attributes = request.text
        msg = 'status_code:{} {}'.format(request.status_code, error_attributes)
        super(ApiError, self).__init__(msg)


class NoContentError(ApiError):
    def __init__(self, request):
        super(NoContentError, self).__init__(request)


class BadRequestError(ApiError):
    def __init__(self, request):
        super(BadRequestError, self).__init__(request)


class UnauthorizedError(ApiError):
    def __init__(self, request):
        super(UnauthorizedError, self).__init__(request)


class ForbiddenError(ApiError):
    def __init__(self, request):
        super(ForbiddenError, self).__init__(request)


class NotFoundError(ApiError):
    def __init__(self, request):
        super(NotFoundError, self).__init__(request)


class NotAcceptableError(ApiError):
    def __init__(self, request):
        super(NotAcceptableError, self).__init__(request)


class ConflictError(ApiError):
    def __init__(self, request):
        super(ConflictError, self).__init__(request)


class UnsupportedMediaError(ApiError):
    def __init__(self, request):
        super(UnsupportedMediaError, self).__init__(request)


class TooManyRequestsError(ApiError):
    def __init__(self, request):
        super(TooManyRequestsError, self).__init__(request)


class ErrorFactory(object):
    factory_objects = {204: NoContentError,
                       400: BadRequestError,
                       401: UnauthorizedError,
                       403: ForbiddenError,
                       404: NotFoundError,
                       406: NotAcceptableError,
                       409: ConflictError,
                       415: UnsupportedMediaError,
                       429: TooManyRequestsError}

    @classmethod
    def compose(cls, request):
        constructor = cls.factory_objects.get(request.status_code, ApiError)
        return constructor(request) if constructor else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
