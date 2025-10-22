from django.urls import include, path
from rest_framework import routers
from app.auth_user.views import CreateUserViewSet


router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = [
    path("", include(router.urls)),
    path("register", CreateUserViewSet.as_view()),
]