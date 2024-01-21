# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User

from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Viewset for user objects."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
