from rest_framework import routers

from .views import *

router = routers.SimpleRouter()

router.register("reservation-time", ReservationTimeViewSet)
router.register("reservations", ReservationViewSet)
router.register("visits", VisitViewSet)
