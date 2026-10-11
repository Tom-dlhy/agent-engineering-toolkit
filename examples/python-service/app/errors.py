class AppError(Exception):
    pass

class ResourceNotFound(AppError):
    pass

class ExternalUnavailable(AppError):
    pass

class ExternalProtocolError(AppError):
    pass

class ExternalRateLimited(AppError):
    pass
