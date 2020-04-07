from django.conf.urls import url, include
from .views import StatusViewSet, ReportViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=True)

router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]