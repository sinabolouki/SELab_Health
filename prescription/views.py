import hashlib
import random
import string

import django
from django.http import HttpResponse
from rest_framework import viewsets

from user.models import User
from .models import Prescription
from .serializers import PrescriptionSerializer, PatientPrescriptionSerializer, AdminPrescriptionSerializer


class GetByDoctor(viewsets.ViewSet):

    def handle_request(self, request):
        try:
            token = request.data['token']
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        try:
            user = User.objects.get(token=token, isDoctor=True)
        except:
            return HttpResponse('Token not valid', status=409)
        if not user:
            return HttpResponse('Token not valid', status=409)

        if user.token_exp_time < django.utils.timezone.now():
            return HttpResponse('Token expired', status=409)

        if not user.isDoctor:
            return HttpResponse('User not doctor', status=409)

        prescriptions = Prescription.objects.filter(patient__national_code=request.data['nationalCode'])
        prescriptions_ser = PrescriptionSerializer(prescriptions, many=True)
        return HttpResponse(prescriptions_ser.data, status=200)


class AddPrescription(viewsets.ViewSet):

    def handle_request(self, request):
        try:
            token = request.data['token']
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        try:
            user = User.objects.get(token=token)
        except:
            return HttpResponse('Token not valid', status=409)
        if not user:
            return HttpResponse('Token not valid', status=409)

        if user.token_exp_time < django.utils.timezone.now():
            return HttpResponse('Token expired', status=409)

        if not user.isDoctor:
            return HttpResponse('User not doctor', status=409)

        try:
            patient = User.objects.get(national_code=request.data['national_code'], isDoctor=False)
        except:
            return HttpResponse('No Patient with this national code', status=409)

        Prescription.objects.create(patient=patient, prescriber=user, drug_list=request.data['drugs'])
        return HttpResponse('Success', status=200)


class GetByPatient(viewsets.ViewSet):

    def handle_request(self, request):
        try:
            token = request.data['token']
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        try:
            user = User.objects.get(token=token)
        except:
            return HttpResponse('Token not valid', status=409)
        if not user:
            return HttpResponse('Token not valid', status=409)

        if user.token_exp_time < django.utils.timezone.now():
            return HttpResponse('Token expired', status=409)

        prescriptions = Prescription.objects.filter(patient=user)
        prescriptions_ser = PatientPrescriptionSerializer(prescriptions, many=True)
        return HttpResponse(prescriptions_ser.data, status=200)


class GetByAdmin(viewsets.ViewSet):

    def handle_request(self, request):
        try:
            token = request.data['token']
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        try:
            user = User.objects.get(token=token)
        except:
            return HttpResponse('Token not valid', status=409)
        if not user:
            return HttpResponse('Token not valid', status=409)

        if user.token_exp_time < django.utils.timezone.now():
            return HttpResponse('Token expired', status=409)

        if not user.isAdmin:
            return HttpResponse('User not admin', status=409)

        prescriptions = Prescription.objects.all()
        prescriptions_ser = AdminPrescriptionSerializer(prescriptions, many=True)
        return HttpResponse(prescriptions_ser.data, status=200)
