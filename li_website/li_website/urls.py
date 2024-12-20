"""
Django URLs configuration for li_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
import os
from . import views

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('gallery/', include('gallery.urls')),
    path('payments/', include('payments.urls')),
    path('legal-info/', views.legal_info, name='legal_info')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")),)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)