from django.contrib.auth.backends import ModelBackend
import rest_framework_jwt.authentication
from backend.models import Kit, PersonUser

def downcast_user_type(user):
    try:
        return Kit.objects.get(pk=user.pk)
    except:
        pass

    try:
        return PersonUser.objects.get(pk=user.pk)
    except:
        pass

    return user

class PersonOrKitBackend(ModelBackend):
    """
    Backend using ModelBackend, but attempts to "downcast"
    the user into a PersonUser or KitUser.
    """

    def authenticate(self, *args, **kwargs):
        return downcast_user_type(super().authenticate(*args, **kwargs))
        
    def get_user(self, *args, **kwargs):
        return downcast_user_type(super().get_user(*args, **kwargs))

class JSONWebTokenAuthentication(rest_framework_jwt.authentication.JSONWebTokenAuthentication):
    """
    Backend using JSONWebTokenAuthentication, but attempts to "downcast"
    the user into a PersonUser or KitUSer.
    """

    def authenticate_credentials(self, payload):
        return downcast_user_type(super().authenticate_credentials(payload))
