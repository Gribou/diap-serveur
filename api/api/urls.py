from django.urls import path, include
from rest_framework import routers
from profiles.views import ProfileViewSet
from search.views import SearchViewSet
from filetree.views import PictureViewSet
from .views import HealthCheckView

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'search', SearchViewSet, basename="search")
router.register(r'gallery', PictureViewSet, basename="gallery")


urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='healthcheck')
]
