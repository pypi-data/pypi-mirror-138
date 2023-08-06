from abc import ABC, abstractmethod


class Adapter(ABC):
    """Abstract Class for Social Provider Adapter.

    Attributes:
        access_token_url (None): URL that is used for getting access token from social provider.
        profile_url (None): URL that is used for getting profile info from social provider.
    """
    access_token_url = None
    profile_url = None

    @abstractmethod
    def get_access_token_data(self, code: str, grant_type: str, scope: str):
        """Abstract method for exchanging authorization code for access token.

        Args:
            code (str): Authorization code.
            grant_type (str, Optional): Grant type.
            scope (str, Optional): Scope.

        """
        pass

    @abstractmethod
    def get_profile_data(self, access_token: str):
        """Abstract method for exchanging access token for profile info.

        Args:
            access_token (str): Access token.

        """
        pass
