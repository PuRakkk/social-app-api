from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.core.filter_backend import CustomBaseFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class CustomFilterBackendMixin:
    filter_backend = [
        CustomBaseFilterBackend,
        SearchFilter,
        OrderingFilter
    ]


class CoreViewSet(CustomFilterBackendMixin ,viewsets.ModelViewSet):
    filterset_field = "__all__"
    ordering_field = "__all__"
    ordering = "-id"
    permission_classes = [IsAuthenticated]


class CoreListViewSet(CustomFilterBackendMixin, generics.ListAPIView):
    filterset_field = "__all__"
    ordering_field = "__all__"
    ordering = "-id"
    permission_classes = [IsAuthenticated]


class CoreCreateViewSet(CustomFilterBackendMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]


class CoreRetrieveViewSet(CustomFilterBackendMixin, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]


class CoreUpdateViewSet(CustomFilterBackendMixin, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]


class CoreDeleteViewSet(CustomFilterBackendMixin, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
