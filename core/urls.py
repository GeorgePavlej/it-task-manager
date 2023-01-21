from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include  # add this

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.authentication.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path("", include(("apps.home.urls", "apps.home"), namespace="home"))]
