from django.contrib import admin
from django.urls import path
from gateway.views import API

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/main/', API.as_view({'post': 'handle_request'})),
    path('api/profile/', include('user.urls'))
]
