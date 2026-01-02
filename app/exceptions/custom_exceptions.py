from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    """404 - source not found  """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "failure",
                "error": {
                    "code": 404,
                    "message": message
                }
            }
        )


class ValidationError(HTTPException):
    """422 - Validation Error"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "failure",
                "error": {
                    "code": 422,
                    "message": message
                }
            }
        )


class ConflictError(HTTPException):
    """409 - Conflict Error (e.g. duplicate unique field)"""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "failure",
                "error": {
                    "code": 409,
                    "message": message
                }
            }
        )


class UnauthorizedError(HTTPException):
    """401 - Unauthorized Error"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "failure",
                "error": {
                    "code": 401,
                    "message": message
                }
            }
        )


class ForbiddenError(HTTPException):
    """403 - Forbidden Error"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "failure",
                "error": {
                    "code": 403,
                    "message": message
                }
            }
        )


class ServerError(HTTPException):
    """500 - Server Error"""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "failure",
                "error": {
                    "code": 500,
                    "message": message
                }
            }
        )
