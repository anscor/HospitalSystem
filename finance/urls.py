from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register("pay-types", PayTypeViewSet)
router.register("pay-records", PayRecordViewSet)
router.register("refund-records", RefundRecordViewSet)
router.register("audit-records", AuditRecordViewSet)
