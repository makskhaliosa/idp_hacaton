from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_v1.views.idp_app import IDPViewSet

router = DefaultRouter()

router.register("idp", IDPViewSet, basename="idp")

urlpatterns = [
    path("v1/", include(router.urls)),
]
