from django.conf.urls import url, include
from .views import StatusViewSet, ReportViewSet, KmGridViewSet,\
    KmGridScoreViewSet, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)
router.register(r'grid', KmGridViewSet)
router.register(r'grid-score', KmGridScoreViewSet)
router.register(r'user', UserViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
]
