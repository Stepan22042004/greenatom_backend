from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import OrganisationViewSet, StorageViewSet, UserViewSet


router = DefaultRouter()

router.register('organisations', OrganisationViewSet)
router.register('storages', StorageViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
