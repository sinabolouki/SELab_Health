from django.contrib import admin
from django.urls import path, include
from gateway.views import API
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/main/', API.as_view({'post': 'handle_request'})),
    path('api/profile/', include('user.urls')),
    path('api/prescription/', include('prescription.urls')),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/admin/', include('admin.urls'))
]
