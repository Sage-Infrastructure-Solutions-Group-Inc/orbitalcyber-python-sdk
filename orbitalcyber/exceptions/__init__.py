class OrbitalCyberAuthenticationError(Exception):

    def __init__(self, message: str = None):
        self.message = message
        if not self.message:
            self.message = "The API client failed to authenticate."
        super().__init__(message)


class OrbitalCyberUnauthorized(Exception):

    def __init__(self, message: str = None):
        self.message = message
        if not message:
            self.message = "The API client session token is invalid."
        super().__init__(message)


class OrbitalCyberForbidden(Exception):

    def __init__(self, message: str = None):
        self.message = message
        if not self.message:
            self.message = "The API client does not have permission to this Resource."
        super().__init__(message)
