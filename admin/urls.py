from django.urls import path
from .views import *

urlpatterns = [
    path('daily_stats/', DailyStats.as_view({'post': 'handle_request'})),
]