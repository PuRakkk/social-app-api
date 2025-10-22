from app.core.views import CoreCreateViewSet
from app.auth_user.models import QuixShareUser
from app.auth_user.serializers import QuixShareUserSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status


class CreateUserViewSet(CoreCreateViewSet):
    model = QuixShareUser
    queryset = QuixShareUser.objects.all()
    serializer_class = QuixShareUserSerializer
    permission_classes = []

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data

        data = {
            **data,
            "is_staff": False,
            "is_superuser": False
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            **serializer.data
        }

        return Response(response, status=status.HTTP_201_CREATED)

