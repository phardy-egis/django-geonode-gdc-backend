from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'resource_detail', views.ResourceDetailCustomViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/resource_list_json/', views.ResourceCustomListJSONView),
]