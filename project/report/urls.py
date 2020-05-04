from django.conf.urls import url, include
from .views import StatusViewSet, ReportViewSet, KmGridViewSet, KmGridScoreViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)
router.register(r'grid', KmGridViewSet)
router.register(r'grid-score', KmGridScoreViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
