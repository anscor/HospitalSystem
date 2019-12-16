from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register("prescriptions", PrescriptionViewSet)
router.register("medical-records", MedicalRecordViewSet)
