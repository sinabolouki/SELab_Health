import hashlib
import random
import string

import django
from django.http import HttpResponse
from rest_framework import viewsets

from .models import User


class Register(viewsets.ViewSet):
    def handle_request(self, request):
        user = User()
        data = request.data
        try:
            user.name = data['name']
            user.national_code, user.password = data['national_code'], hashlib.md5(data['password'].encode('utf-8')).digest()
            try:
                user.save()
            except django.db.utils.IntegrityError:
                return HttpResponse('Conflict', status=409)
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        return HttpResponse('User created', status=200)


class Login(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            national_code, password = request.data['national_code'], str(request.data['password'])
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        try:
            user = User.objects.get(national_code=national_code)
        except:
            return HttpResponse("Provided Info is wrong!", status=404)
        if str(user.password) == str(hashlib.md5(password.encode('utf-8')).digest()):
            if user.token_exp_time > django.utils.timezone.now():
                return HttpResponse(user.token, status=200)
            else:
                user.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
                user.token_exp_time = django.utils.timezone.now() + django.utils.timezone.timedelta(hours=1, minutes=30)
                user.save()
                return HttpResponse(user.token, status=200)
        else:
            return HttpResponse("Provided Info is wrong!", status=404)


class Profile(viewsets.ViewSet):
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

        if 'profile' in request.data:
            user.profile = request.data['profile']
            user.save()

        return HttpResponse('your profile: ' + user.profile, status=200)
