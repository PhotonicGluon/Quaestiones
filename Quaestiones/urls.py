"""
urls.py

Created on 2020-12-26
Updated on 2021-02-06

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the website.
"""

# IMPORTS
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Quaestiones.views import faviconView, info_view

# URL CONFIG
urlpatterns = [
    path("favicon.ico", faviconView),
    path("info/", info_view, name="info"),
    path("", include("accounts.urls")),
    path("console/", include("console.urls")),
    path("", include("questions.urls")),
    path("", include("stats.urls")),
    path("", include("uploaded_files_manager.urls")),
    path("admin/", admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ERROR HANDLING
handler400 = "Quaestiones.views.error400"
handler403 = "Quaestiones.views.error403"
handler404 = "Quaestiones.views.error404"
handler500 = "Quaestiones.views.error500"
