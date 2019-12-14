from rest_framework import routers

from .views import *

router = routers.SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", GroupViewSet)
router.register("occupations", OccupationViewSet)
router.register("user-logs", UserLogRecordViewSet)
router.register("black-list", BlackListViewSet)
