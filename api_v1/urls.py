from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_v1.views.idp_app import (
    DepartmentViewSet,
    FileViewSet,
    IDPNotificationViewSet,
    IDPViewSet,
    NotificationViewSet,
    TaskNotificationViewSet,
    TaskViewSet,
)
from api_v1.views.users import UserViewSet

router = DefaultRouter()

router.register(
    r"idp/(?P<idp_id>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/tasks",
    TaskViewSet,
    basename="tasks",
)
router.register("department", DepartmentViewSet, basename="department")
router.register("file", FileViewSet, basename="file")
router.register("notification", NotificationViewSet, basename="notification")
router.register("idp", IDPViewSet, basename="idp")
router.register(
    "idp-notification", IDPNotificationViewSet, basename="idp-notification"
)
router.register(
    "task-notification", TaskNotificationViewSet, basename="task-notification"
)
router.register("users", UserViewSet, basename="users")


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
