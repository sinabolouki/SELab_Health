from django.urls import path
from .views import *

urlpatterns = [
    path('register/', Register.as_view({'post': 'handle_request'})),
    path('login/', Login.as_view({'post': 'handle_request'})),
    path('', Profile.as_view({'post': 'handle_request'}))
]
