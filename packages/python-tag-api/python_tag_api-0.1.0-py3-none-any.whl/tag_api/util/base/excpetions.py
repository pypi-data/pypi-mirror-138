class TagApiException(Exception):
    """
    Tag Api Error

    Parameters:
        error_code: integer HTTP Error code returned in the response
        errors: list(str) All errors TAG found on the request
        process_key: str TAG's internal process key for the request
        created_at: datetime when TAG received the request
    """

    def __init__(self, http_error_code, errors, process_key, created_at):
        self.http_error_code = http_error_code
        self.errors = errors
        self.process_key = process_key
        self.created_at = created_at


class UnauthorizedException(Exception):
    """
    Generic error when not authorized

    Parameters:
        http_status_code: integer HTTP Status code returned in the response from TAG Auth Endpoint
        error: str the field 'error' from TAG response object
        error_description: str the 'error_description' field from TAG response object
    """

    def __init__(self, http_status_code, error, error_description):
        self.http_status_code = http_status_code
        self.error = error
        self.error_descprition = error_description