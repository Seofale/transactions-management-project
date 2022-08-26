from rest_framework import generics

from ..serializers import UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
