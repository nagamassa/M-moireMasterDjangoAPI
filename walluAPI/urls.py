
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wallu.urls')),
    path('checkserver/', views.index, name='index'),
    path('auth/', include('authapp.urls')),

]

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)