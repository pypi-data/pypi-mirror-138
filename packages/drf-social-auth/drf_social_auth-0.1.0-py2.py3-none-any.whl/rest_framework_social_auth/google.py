import requests
from django.conf import settings

from rest_framework_social_auth.adapter import Adapter
from rest_framework_social_auth.views import SocialLoginView


class GoogleAdapter(Adapter):
    """Custom Adapter for Google Social Authentication.

    Attributes:
        access_token_url (str): URL that is used for getting access token from social provider.
        profile_url (str): URL that is used for getting profile info from social provider.
    """
    access_token_url = "https://accounts.google.com/o/oauth2/token"
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    def get_access_token_data(self, code: str, grant_type: str, scope: str):
        """Method for exchanging authorization code for access token.

        Here we specify all necessary info (i.e. client_id, client_secret) for Google provider
        and send request to `access_token_url` to get access token.

        Args:
            code (str): Authorization code.
            grant_type (str, Optional): Grant type.
            scope (str, Optional): Scope.

        """
        GOOGLE_CLIENT_ID = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        GOOGLE_CLIENT_SECRET = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
        GOOGLE_REDIRECT_URI = getattr(settings, 'GOOGLE_REDIRECT_URI', None)

        if not (GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET or GOOGLE_REDIRECT_URI):
            raise ValueError('You must specify `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`\
                             and `GOOGLE_REDIRECT_URI` in your settings.')

        data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'code': code,
            'scope': scope,
            'grant_type': grant_type
        }
        resp = requests.post(self.access_token_url, data=data)
        access_token = resp.json().get('access_token', None)
        return access_token

    def get_profile_data(self, access_token: str):
        """Method for exchanging access token for profile info.

        Here we use `access_token` to get Google account's profile info.

        Args:
            access_token (str): Access token.

        """
        resp = requests.get(
            self.profile_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_info = resp.json()
        return profile_info


class GoogleLogin(SocialLoginView):
    """View for retrieving Google account profile info.

    Attributes:
        adapter (GoogleAdapter()): GoogleAdapter that is used to define settings for Google social authentication.
    """
    adapter = GoogleAdapter()
