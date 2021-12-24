from django.urls import path
from .views import *

urlpatterns = [
    path('get_by_doctor/', GetByDoctor.as_view({'post': 'handle_request'})),
    path('add/', AddPrescription.as_view({'post': 'handle_request'})),
    path('get_by_patient/', GetByPatient.as_view({'post': 'handle_request'})),
    path('get_by_admin/', GetByAdmin.as_view({'post': 'handle_request'}))
]
