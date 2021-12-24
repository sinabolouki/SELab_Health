from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Prescription


class PrescriptionSerializer(ModelSerializer):
    patient_name = serializers.CharField(source='patient.name')

    class Meta:
        model = Prescription
        fields = ['prescriber', 'patient', 'drug_list', 'creation_date', 'patient_name']


class PatientPrescriptionSerializer(ModelSerializer):
    prescriber_name = serializers.CharField(source='prescriber.name')

    class Meta:
        model = Prescription
        fields = ['prescriber', 'patient', 'drug_list', 'creation_date', 'prescriber_name']


class AdminPrescriptionSerializer(ModelSerializer):
    prescriber_name = serializers.CharField(source='prescriber.name')
    patient_name = serializers.CharField(source='patient.name')

    class Meta:
        model = Prescription
        fields = ['prescriber', 'patient', 'drug_list', 'creation_date', 'prescriber_name', 'patient_name']