from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import Patient,PatientSiezure

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username','first_name', 'last_name', 'email','password')


class PatientSerializer(serializers.ModelSerializer):
    p_id = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Patient
        fields = ('p_id', 'name', 'birthdate', 'gender', 'contact','emergency_contact1','emergency_contact2','current_GPS','email')


class PatientSiezureSerializer(serializers.ModelSerializer):
    p_id = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = PatientSiezure
        fields = ('p_id', 'time_of_siezure', 'siezure_GPS')

