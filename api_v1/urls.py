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

router = DefaultRouter()

router.register("task", TaskViewSet, basename="task")
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


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.jwt")),
]
