from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from project.report.views import mvt_view_factory, StatusViewSet, ReportViewSet, UserViewSet
from django.urls import path, include, re_path
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
router = DefaultRouter(trailing_slash=True)
router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-v1'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('', include(router.urls)),
    path("grid-score-tiles/", mvt_view_factory(KmGridScore)),
]
