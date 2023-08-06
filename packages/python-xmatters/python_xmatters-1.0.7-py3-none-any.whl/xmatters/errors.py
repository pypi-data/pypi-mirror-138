class Error(Exception):
    pass


class XMSessionError(Error):
    def __init__(self, msg):
        super(XMSessionError, self).__init__(msg)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuthorizationError(Error):
    def __init__(self, msg):
        super(AuthorizationError, self).__init__(msg)


class ApiError(Error):
    def __init__(self, status_code, data):
        if isinstance(data, dict):
            error_attributes = ' '.join(['{}: {}'.format(k, v) for k, v in data.items()])
        else:
            error_attributes = data
        msg = 'status_code:{} {}'.format(status_code, error_attributes)
        super(ApiError, self).__init__(msg)


class NoContentError(ApiError):
    def __init__(self, status_code, data):
        super(NoContentError, self).__init__(status_code, data)


class BadRequestError(ApiError):
    def __init__(self, status_code, data):
        super(BadRequestError, self).__init__(status_code, data)


class UnauthorizedError(ApiError):
    def __init__(self, status_code, data):
        super(UnauthorizedError, self).__init__(status_code, data)


class ForbiddenError(ApiError):
    def __init__(self, status_code, data):
        super(ForbiddenError, self).__init__(status_code, data)


class NotFoundError(ApiError):
    def __init__(self, status_code, data):
        super(NotFoundError, self).__init__(status_code, data)


class NotAcceptableError(ApiError):
    def __init__(self, status_code, data):
        super(NotAcceptableError, self).__init__(status_code, data)


class ConflictError(ApiError):
    def __init__(self, status_code, data):
        super(ConflictError, self).__init__(status_code, data)


class UnsupportedMediaError(ApiError):
    def __init__(self, status_code, data):
        super(UnsupportedMediaError, self).__init__(status_code, data)


class TooManyRequestsError(ApiError):
    def __init__(self, status_code, data):
        super(TooManyRequestsError, self).__init__(status_code, data)


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
    def compose(cls, status_code, item_data):
        constructor = cls.factory_objects.get(status_code, ApiError)
        return constructor(status_code, item_data) if constructor else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
