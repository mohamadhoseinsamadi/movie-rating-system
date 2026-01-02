"""
Custom exceptions for the Movie Rating System
"""


class NotFoundError(Exception):
    """Exception raised when a resource is not found"""
    pass


class ValidationError(Exception):
    """Exception raised when validation fails"""
    pass

