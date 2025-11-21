import random
from rest_framework.serializers import ValidationError
from app.auth_user.models import QuixShareUser


class UserDataProcessor:
    def __init__(self):
        pass

    def prepare_user_data(cls, request):
        data = request.data
        cls.email_validator(data)
        cls.password_validator(data)

        return {
            **data,
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "otp": cls.generate_otp(),
        }

    def generate_otp(cls):
        return str(random.randint(100000, 999999))

    def email_validator(cls, data):
        if QuixShareUser.objects.filter(email=data.get("email")).exists():
            raise ValidationError({"email": "Email is already exist."})
        
    def password_validator(cls, data):
        if len(data.get("password", "")) < 6:
            raise ValidationError({"password": "Password must be at least 6 charactors"})