from django.contrib import admin, auth
from django.urls import path, re_path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api-auth", include("rest_framework.urls", namespace="rest_framework")
    ),
    re_path(r"^", include("User.urls")),
    re_path(r"^", include("Finance.urls")),
    re_path(r"^", include("Medicine.urls")),
    re_path(r"^", include("Outpatient.urls")),
    re_path(r"^", include("Laboratory.urls")),
    re_path(r"^", include("Reservation.urls")),
]
