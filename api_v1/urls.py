from django.urls import include, path
from api_v1.views.idp_app import TaskViewSet, DepartmentViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('task', TaskViewSet, basename='task')
router.register('department', DepartmentViewSet, basename='department')

urlpatterns = [
    path("v1/", include(router.urls)),
]
