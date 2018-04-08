from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.models import Patient,PatientSiezure
from api.permissions import IsOwnerOrReadOnly
from api.serializers import PatientSerializer, PatientSiezureSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

class PatientProfile(APIView):


    def get_object(self, pk):
        try:
            return Patient.objects.all().filter(username=pk)
        # profile=Profile.objects.all()[0]

        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        uname=request.user.username
        profile = Patient.objects.get(p_id__username=uname)
        serializer = PatientSerializer(profile)
        if profile is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request,pk=None,format=None):
        uname=request.user.username
        profile = Patient.objects.get(p_id__username=uname)
        req = request.data
        # self.request.user.
        serializer = PatientSerializer(profile, data=req,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,format=None):
        print request.user.username
        try:
            Patient.objects.get(p_id__username=request.user.username)
            return Response("Patient Exists! Cannot create new!", status=status.HTTP_400_BAD_REQUEST)

        except:
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(p_id=User.objects.get(username=request.user.username))
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientSiezures(APIView):

    def get(self, request, format=None):
        uname = request.user.username
        siezures =  PatientSiezure.objects.all().filter(p_id__username=uname)
        serializer = PatientSiezureSerializer(siezures,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
           # return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self,request,format=None):

        serializer = PatientSiezureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(p_id=User.objects.get(username=request.user.username))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



