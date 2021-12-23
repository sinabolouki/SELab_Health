from django.http import HttpResponse
import requests
from django.http import HttpResponse
from rest_framework import viewsets
from . import service_consts

failed_attempts = {
    service_consts.user_register: 0, service_consts.user_login: 0,
    service_consts.user_profile: 0
}


class API(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service == service_consts.user_register:
            if failed_attempts[service_consts.user_register] < 3:
                return self.register(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == service_consts.user_login:
            if failed_attempts[service_consts.user_login] < 3:
                return self.login(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == service_consts.user_profile:
            if failed_attempts[service_consts.user_profile] < 3:
                return self.profile(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def register(data):
        url = 'http://127.0.0.1:8000/api/profile/register/'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_attempts[service_consts.user_register] += 1
            return HttpResponse('Service Unavailable', status=503)
        if response.status_code / 100 == 5:
            failed_attempts[service_consts.user_register] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def login(data):
        url = 'http://127.0.0.1:8000/api/profile/login/'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_attempts[service_consts.user_login] += 1
            return HttpResponse('Service Unavailable', status=503)
        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_attempts[service_consts.user_login] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def profile(data):
        url = 'http://127.0.0.1:8000/api/profile/'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_attempts[service_consts.user_profile] += 1
            return HttpResponse('Service Unavailable', status=503)
        if response.status_code / 100 == 5:
            failed_attempts[service_consts.user_profile] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

