from datetime import datetime, timedelta, time
import django
from django.http import HttpResponse
from rest_framework import viewsets, fields, serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes

from user.models import User
from prescription.models import Prescription

from .serializers import UserSerializer

class DailyStats(viewsets.ViewSet):
    @extend_schema(
        request=inline_serializer("daily_status", {'token': fields.CharField(default='token')}),
        description="get daily status",
        responses={'200': inline_serializer('result', {'new_doctors':UserSerializer(many=True), 'new_users': UserSerializer(many=True),
                                             'prescription_count': serializers.IntegerField(default=100)}),
                   '406': OpenApiTypes.STR, '409': OpenApiTypes.STR, '403': serializers.CharField(default='User not admin')}
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

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        new_users = User.objects.filter(sign_up_date__gte=today_start)
        new_users_ser = UserSerializer(new_users, many=True)
        new_doctors = User.objects.filter(sign_up_date__gte=today_start, isDoctor=True)
        new_doctors_ser = UserSerializer(new_doctors, many=True)
        prescription_count = Prescription.objects.filter(creation_date__gte=today_start).count()
        data = {'new_doctors': new_doctors_ser.data, 'new_users': new_users_ser.data,
                'prescription_count': prescription_count}
        return HttpResponse(data, status=200)
