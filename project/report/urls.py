from django.conf.urls import url, include
from .views import StatusViewSet, ReportViewSet, KmGridViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=True)

router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)
router.register(r'grid', KmGridViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
