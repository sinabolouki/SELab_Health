import requests
from django.http import HttpResponse
from rest_framework import viewsets

from . import service_consts

failed_attempts = {
    service_consts.user_register: 0, service_consts.user_login: 0,
    service_consts.user_profile: 0, service_consts.doctor_add_prescription: 0,
    service_consts.doctor_list_prescriptions: 0, service_consts.patient_list_prescriptions: 0,
    service_consts.admin_list_prescriptions: 0, service_consts.admin_get_daily: 0
}


class API(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service not in service_consts.service_urls:
            return HttpResponse('Bad Request', status=400)
        else:
            if failed_attempts[service] < 3:
                return self.send_request(request.data, service_consts.service_urls[service], service)
            else:
                return HttpResponse('Service Unavailable', status=503)

    @staticmethod
    def send_request(data, url, service_name):
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_attempts[service_name] += 1
            return HttpResponse('Service Unavailable', status=503)
        if response.status_code / 100 == 5:
            failed_attempts[service_name] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

