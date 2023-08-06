# drf_social_auth

drf_social_auth is an ultra-lightweight solution for social authentication support in Django REST Framework.
And it supports Google Authentication out-of-box.

---

**Source code** [https://github.com/coaxsoft/drf-social-auth/](https://github.com/coaxsoft/drf-social-auth/)

---

## Requirements

-  Python 3.6+
-  Django 3.0+
-  Django REST Framework 3.11+

## Installation
`pip install drf-social-auth`

## Usage

### Use built-in Google Authentication
1. You must specify the following Google settings in your `settings.py`:
```
GOOGLE_CLIENT_ID= 
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
```
2. Add the following to your `urls.py`.
```
from rest_framework_social_auth.google import GoogleLogin

urlpatterns = [
    path('google/', GoogleLogin.as_view(), name='google-login')
]
```

4. It's done! You can send your `code`, `grant_type` and `scope` (if any) to this endpoint to retrieve profile info from Google Account.

### Create your own solution for other social authentication provider

1. You need to create an adapter for your provider.

This can be done by inheriting from `Adapter` abstract class and overriding `get_access_token_data` and `get_profile_data` methods.

You should also specify `access_token_url` and `profile_url` endpoints.

It is better to use `GoogleAdapter` in `rest_framework_social_auth.google` as an example.

```
from rest_framework_social_auth.adapter import Adapter

class YourProviderAdapter(Adapter):
    pass
```

2. Now you need to create a View and specify your adapter.
```  
from rest_framework_social_auth.views import SocialLoginView

class YourProviderLogin(SocialLoginView):
    adapter = YourProviderAdapter()
```

3. Create an endpoint in `urls.py` using your View and you are good to go.

## Testing
`tox`

## License

This project is licensed under the terms of the ISC License