from django.urls import path, include
from .views import DetailsViewSet, TopicCategoryGDCViewSet, GeoJSONViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'details', DetailsViewSet)
router.register(r'categories', TopicCategoryGDCViewSet)
router.register(r'geojson', GeoJSONViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/resource_list_json/', views.ResourceCustomListJSONView),
]