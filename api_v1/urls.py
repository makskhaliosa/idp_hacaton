from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_v1.views.idp_app import DepartmentViewSet, IDPViewSet, TaskViewSet
from api_v1.views.users import UserViewSet

router = DefaultRouter()

router.register("idp", IDPViewSet, basename="idp")
router.register("task", TaskViewSet, basename="task")
router.register("department", DepartmentViewSet, basename="department")
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.jwt")),
]
