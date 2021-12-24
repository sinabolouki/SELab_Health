from django.contrib import admin
from django.urls import path, include
from gateway.views import API
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/main/', API.as_view({'post': 'handle_request'})),
    path('api/profile/', include('user.urls')),
    path('api/prescription/', include('prescription.urls')),
    path('api/swagger/', schema_view)
]
