from .models import User
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class UserService:
    @staticmethod
    def create_member_user(username, email, password):
        try:
            user = User.objects.create_user(
                username = username,
                email = email,
                password = password,
            )

            user.role = "MEMBER"
            user.is_active = True
            user.save()
            return user
        
        except IntegrityError:
            raise ValidationError({
                "detail": "User with this username or email already exists."
            })
        