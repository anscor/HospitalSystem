from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('User.urls')),
    re_path(r'^', include('Finance.urls')),
    re_path(r'^', include('Medicine.urls')),
    re_path(r'^', include('Outpatient.urls')),
]
