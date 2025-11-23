from django.contrib.auth import get_user_model

class EmailBackend:
    """Authenticate using an email address.

    Notes:
    - This backend assumes User.email is unique across users. Make sure you enforce unique emails when creating accounts.
    - Falls back to default behavior if no user found.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Django's auth views send the login value as 'username' by default.
        email = username or kwargs.get('email')
        UserModel = get_user_model()
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        # Mirrors Django's default: allow active users only
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
