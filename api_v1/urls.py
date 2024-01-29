from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_v1.views.idp_app import (
    DepartmentViewSet,
    FileViewSet,
    IDPViewSet,
    TaskViewSet,
)

router = DefaultRouter()

router.register("idp", IDPViewSet, basename="idp")
router.register("task", TaskViewSet, basename="task")
router.register("department", DepartmentViewSet, basename="department")
router.register("file", FileViewSet, basename="file")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.jwt")),
    path(
        "v1/download/<int:file_id>/",
        FileViewSet.as_view({"get": "download_file"}),
        name="download_file",
    ),
]
