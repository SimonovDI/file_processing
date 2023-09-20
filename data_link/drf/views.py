from rest_framework import generics
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DRF
from .serializers import DRFSerializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class DrfApiViews(generics.ListAPIView):
    serializer_class = DRFSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = DRF.objects.all()
        return queryset


class AuthenticationView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
