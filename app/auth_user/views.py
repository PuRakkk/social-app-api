from app.core.views import CoreCreateViewSet
from app.auth_user.models import QuixShareUser
from app.auth_user.serializers import QuixShareUserSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate
from django.utils.timezone import now
from app.core.exceptions import BadRequestException
from app.auth_user.services import UserDataProcessor

class CreateUserViewSet(CoreCreateViewSet):
    model = QuixShareUser
    queryset = QuixShareUser.objects.all()
    serializer_class = QuixShareUserSerializer
    permission_classes = []

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        user_data_processor = UserDataProcessor()

        data = user_data_processor.prepare_user_data(request)
        serializer, instance = self.process_user_creation(data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def process_user_creation(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        instance.set_password(data.get("password"))
        instance.save()
        return serializer, instance

class UserLoginViewSet(CoreCreateViewSet):
    model = QuixShareUser
    queryset = QuixShareUser.objects.all()
    serializer_class = QuixShareUserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        user_email = QuixShareUser.objects.filter(email=email).first()
        attempts_login_key = f"attempt_login_{email}"

        punish_user = user_email.objects.filter(attempts_time__gte=now()).first()
        if punish_user:
            total_second = (punish_user.attempts_time - now()).total_seconds()
            minutes = int(total_second // 60)
            seconds = int(total_second % 60)
            raise BadRequestException(
                f"Too many failed attempts. Try again in {minutes} minutes {seconds} seconds."
            )


        
        