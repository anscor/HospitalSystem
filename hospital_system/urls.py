from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from finance.urls import router as finance_router
from laboratory.urls import router as laboratory_router
from medicine.urls import router as medicine_router
from outpatient.urls import router as outpatient_router
from reservation.urls import router as reservation_router
from user.urls import router as user_router

from user.views import logout

router = routers.DefaultRouter()

router.registry.extend(finance_router.registry)
router.registry.extend(laboratory_router.registry)
router.registry.extend(medicine_router.registry)
router.registry.extend(outpatient_router.registry)
router.registry.extend(reservation_router.registry)
router.registry.extend(user_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", TokenObtainPairView.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),
    path("api/auth/logout/", logout.as_view()),
]
