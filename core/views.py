from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import UserProfile, BookExchange, Book
from .serializer import UserSerializer, BookSerializer, BookExchangeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookExchangeViewSet(viewsets.ModelViewSet):
    queryset = BookExchange.objects.all()
    serializer_class = BookExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
