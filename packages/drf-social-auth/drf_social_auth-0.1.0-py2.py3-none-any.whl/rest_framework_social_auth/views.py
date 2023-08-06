from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_social_auth.serializers import SocialLoginSerializer


class SocialLoginView(GenericAPIView):
    """Abstract View for retrieving profile info.

    The process of getting profile info is divided into two steps.

    In the first step, we send the parameters to get the access token.
    In the second step, we exchange the access token for profile data.

    Attributes:
        permission_classes (AllowAny,): Permission classes.
        serializer_class (SocialLoginSerializer): Serializer.
        adapter (None): Adapter that is used to define settings for particular social provider.
    """
    permission_classes = (AllowAny,)
    serializer_class = SocialLoginSerializer
    adapter = None

    def post(self, request, *args, **kwargs):
        """Post method

           Args:
               request: request.
               args: arguments.
               kwargs: keyword arguments.

           Returns:
               Profile Info if successful, HTTP_400_BAD_REQUEST otherwise.

        """
        self.serializer = self.get_serializer(data=self.request.data)
        if self.serializer.is_valid(raise_exception=True):
            code = self.serializer.validated_data.get('code')
            grant_type = self.serializer.validated_data.get('grant_type')
            scope = self.serializer.validated_data.get('scope')
            access_token = self.adapter.get_access_token_data(code=code, grant_type=grant_type, scope=scope)
            profile_info = self.adapter.get_profile_data(access_token)
            return Response(profile_info)
        return Response(status=status.HTTP_400_BAD_REQUEST)
