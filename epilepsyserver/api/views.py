from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.models import Patient
from api.permissions import IsOwnerOrReadOnly
from api.serializers import PatientSerializer, PatientSiezureSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

class PatientProfile(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    def get_object(self, pk):
        try:
            return Patient.objects.get(pk=pk)
        # profile=Profile.objects.all()[0]

        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = PatientSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # data= JSONParser().parse(request)
        profile = self.get_object(pk)
        req = request.data
        req['p_id'] = self.request.user.username
        # self.request.user.

        serializer = PatientSerializer(profile, data=req)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientSiezures(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return PatientSiezures.objects.all().filter(p_id=pk)
        # profile=Profile.objects.all()[0]

        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        siezures = self.get_object(pk)
        serializer = PatientSiezureSerializer(siezures)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # data= JSONParser().parse(request)
        profile = self.get_object(pk)
        req = request.data
        req['p_id'] = self.request.user.username
        # self.request.user.

        serializer = PatientSerializer(profile, data=req)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

