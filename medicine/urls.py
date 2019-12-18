from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register("medicine-types", MedicineTypeViewSet)
router.register("medicine", MedicineViewSet)
router.register("medicine-handout-records", MedicineHandoutRecordViewSet)
