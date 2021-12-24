import hashlib
import random
import string

import django
from django.http import HttpResponse
from rest_framework import viewsets, fields
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes


from user.models import User
from .models import Prescription
from .serializers import PrescriptionSerializer, PatientPrescriptionSerializer, AdminPrescriptionSerializer


class GetByDoctor(viewsets.ViewSet):

    @extend_schema(
        request=inline_serializer("doctors_patient_prescriptions", {'national_code': fields.CharField(default='0022334455'), 'token': fields.CharField(default='token')},),
        description="get patient's prescriptions by doctor",
        responses={'200': PrescriptionSerializer(many=True), '406': OpenApiTypes.STR, '409': OpenApiTypes.STR,
                    '403': OpenApiTypes.STR}
    )
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
            return HttpResponse('User not doctor', status=403)

        prescriptions = Prescription.objects.filter(patient__national_code=request.data['national_code'])
        prescriptions_ser = PrescriptionSerializer(prescriptions, many=True)
        return HttpResponse(prescriptions_ser.data, status=200)


class AddPrescription(viewsets.ViewSet):

    @extend_schema(
        request=inline_serializer("add_prescription_serializer", {'national_code': fields.CharField(default='0022334455'), 'token' : fields.CharField(default='token'),
                                              'drugs': fields.CharField(default="['acentra', 'acetaminophene']")}),
        description="add a prescription",
        responses={'200': PrescriptionSerializer(), '406': OpenApiTypes.STR, '409': OpenApiTypes.STR,
                    '403': OpenApiTypes.STR, '404': OpenApiTypes.STR, }
    )
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
            return HttpResponse('No Patient with this national code', status=404)

        prescription = Prescription.objects.create(patient=patient, prescriber=user, drug_list=request.data['drugs'])
        return HttpResponse(PrescriptionSerializer(prescription), status=200)


class GetByPatient(viewsets.ViewSet):

    @extend_schema(
        request=inline_serializer("get_patient_prescriptions", {'token': fields.CharField(default='token')},),
        description="get patient's prescriptions",
        responses={'200': PatientPrescriptionSerializer(many=True), '406': OpenApiTypes.STR, '409': OpenApiTypes.STR}
    )
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

    @extend_schema(
        request=inline_serializer("admin_prescriptions", {'token': fields.CharField(default='token')}),
        description="get all prescriptions",
        responses={'200': AdminPrescriptionSerializer(many=True), '406': OpenApiTypes.STR, '409': OpenApiTypes.STR,
                   '403': OpenApiTypes.STR}
    )
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
            return HttpResponse('User not admin', status=403)

        prescriptions = Prescription.objects.all()
        prescriptions_ser = AdminPrescriptionSerializer(prescriptions, many=True)
        return HttpResponse(prescriptions_ser.data, status=200)
