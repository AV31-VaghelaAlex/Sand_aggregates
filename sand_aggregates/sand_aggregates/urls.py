"""
URL configuration for sand_aggregates project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls', namespace='website')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Admin site header and titles
admin.site.site_header = "Sand Aggregates Administration"
admin.site.site_title = "Sand Aggregates Admin Portal"
admin.site.index_title = "Welcome to Sand Aggregates Management System"
