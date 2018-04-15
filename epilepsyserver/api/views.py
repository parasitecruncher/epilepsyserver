import json
from collections import defaultdict
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from api.models import Patient,PatientSiezure
from api.permissions import IsOwnerOrReadOnly
from api.serializers import PatientSerializer, PatientSiezureSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
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

        try:
            Patient.objects.get(p_id__username=request.user.username)
            return Response("Patient Exists! Cannot create new!", status=status.HTTP_400_BAD_REQUEST)

        except:
            serializer = PatientSerializer(data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(p_id=User.objects.get(username=request.user.username))
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        if Patient.objects.all().filter(p_id__username=request.data['username']).count() == 1:
            print request.data['username']
            return Response("Patient Exists! Cannot create new!", status=status.HTTP_400_BAD_REQUEST)

        else:
            if User.objects.filter(username=request.data['username']).count()==0:
                newuser=User(username=request.data['username'],
                             email=request.data['email'])
                newuser.set_password(request.data['password'])
                newuser.save()
            newuser=User.objects.get(username=request.data['username'])
            serializer = PatientSerializer(data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(p_id=User.objects.get(username=newuser.username))
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

class PatientSiezuresFrequency(APIView):

    def post(self, request, format=None):
        uname = request.user.username
        siezures =  PatientSiezure.objects.all().filter(p_id__username=uname)
        freqtable=defaultdict(int)
        if request.data['type']=="day":
            for siezure in siezures:
                time=siezure.time_of_siezure.split()
                freqtable[""+time[2]+time[1]+time[5]]+=1
            pass
        elif request.data['type']=="month":
            for siezure in siezures:
                time=siezure.time_of_siezure.split()
                freqtable[""+time[1]+time[5]]+=1
        elif request.data['type']=="year":
            for siezure in siezures:
                time=siezure.time_of_siezure.split()
                freqtable[time[5]]+=1
        data=json.dumps(freqtable)
        if len(freqtable)>0:
            return HttpResponse(data, content_type='application/json')
        return Response(status=status.HTTP_204_NO_CONTENT)

