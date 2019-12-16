from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register("laboratory-types", LaboratoryTypeViewSet)
