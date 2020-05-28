from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework import permissions
from rest_framework_mvt.views import mvt_view_factory
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from project.report.views import StatusViewSet, ReportViewSet, KmGridViewSet,\
    KmGridScoreViewSet, UserViewSet
from project.report.models.km_grid_score import KmGridScore

router = DefaultRouter()
router.register(r'status', StatusViewSet)
router.register(r'report', ReportViewSet)
router.register(r'grid', KmGridViewSet)
router.register(r'grid-score', KmGridScoreViewSet)
router.register(r'user', UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="How Am I Doing? API",
        default_version='v1',
        description="Backend for How Am I Doing? app",
        terms_of_service="https://kartoza.com/en/about/",
        contact=openapi.Contact(email="info@kartoza.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path('admin/', admin.site.urls),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(router.urls)),
    path("api/v1/grid-score-tiles/", mvt_view_factory(KmGridScore)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
