from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'details', views.DetailsViewSet)
router.register(r'categories', views.CategoriesViewSet)
router.register(r'geojson', views.GeoJSONViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/resource_list_json/', views.ResourceCustomListJSONView),
]