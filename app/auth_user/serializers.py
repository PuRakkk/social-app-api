from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from app.auth_user.models import QuixShareUser, QuixShareUserProfile
from rest_framework.validators import UniqueValidator

class QuixShareProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuixShareUserProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "username",
            "status",
        ]

    def to_internal_value(self, data):
        if self.instance:
            data["email"] = self.email
            if self.instance.status == "active":
                data["email"] = self.instance.status

        return super().to_internal_value(data)
    
    

class QuixShareUserSerializer(WritableNestedModelSerializer):
    quix_share_user_profile = QuixShareProfileSerializer()
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=QuixShareUser.objects.all(),
                message="This email is already registered"
            )
        ]
    )
    class Meta:
        model = QuixShareUser
        exclude = [
            "is_staff",
            "password",
            "last_login",
            "created_at",
            "updated_at",
        ]
        extra_kwarge = {
            "password": {"write_only", True},
        }

    def to_internal_value(self, data):
        if self.instance:
            data = {
                **data,
                "is_staff": self.instance.is_staff,
                "is_superuser": self.instance.is_superuser,
                "password": self.instance.password,
                "username": self.instance.username,
            }
        else:
            data["quix_share_user_profile"]["email"] = data.get("email")

        return super().to_internal_value(data)