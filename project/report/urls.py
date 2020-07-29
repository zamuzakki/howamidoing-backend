from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_mvt.views import mvt_view_factory
from django.urls import path, include, re_path
from .views import StatusViewSet, ReportViewSet, KmGridViewSet,\
    KmGridScoreViewSet, UserViewSet
from .api_views.report_point import ReportPointViewSet
from .api_views.report_point_score import ReportPointScoreViewSet
from project.report.models.km_grid_score import KmGridScore
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="How Am I Doing? API",
        default_version='v1',
        description="Backend for How Am I Doing? app",
        terms_of_service="https://kartoza.com/en/about/",
        contact=openapi.Contact(email="info@kartoza.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)
router = DefaultRouter(trailing_slash=False)
router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)
# router.register(r'report-point', ReportPointViewSet)
# router.register(r'report-score', ReportPointScoreViewSet)
router.register(r'grid', KmGridViewSet)
router.register(r'grid-score', KmGridScoreViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path('v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-v1'),
    path('redoc/v1/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('v1/', include(router.urls)),
    path("v1/grid-score-tiles/", mvt_view_factory(KmGridScore)),
]
