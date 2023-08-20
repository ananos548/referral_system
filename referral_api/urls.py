from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import UserProfileViewSet

router = SimpleRouter()
router.register(r'profile', UserProfileViewSet, basename='userprofile')


urlpatterns = [
]

urlpatterns += router.urls