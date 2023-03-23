from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'resource_detail', views.ResourceDetailCustomViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path(r'api/resource_list/', views.ResourceCustomListView.as_view()),
]