# Django base
from .serializers import *
from geonode.layers.models import Dataset
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TopicCategoryGDC
from django_filters import rest_framework as filters
from shapely import geometry as shapely_geometry
from rest_framework import filters as drf_filters

from geonode.base.api.permissions import (
    UserHasPerms,
)
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class DetailsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to filter geo-spatial data catalogue results
    """
    # permission_classes = [IsAuthenticated, UserHasPerms]
    queryset = Dataset.objects.all()
    serializer_class = DetailsSerializer
    pagination_class = StandardResultsSetPagination

# API entrypoint for variable objects
class TopicCategoryGDCViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that lists categories and their SVG icons.
    """
    # permission_classes = [IsAuthenticated]
    queryset = TopicCategoryGDC.objects.all().order_by('position_index')
    serializer_class = TopicCategoryGDCSerializer

class GeoJSONViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to filter geo-spatial data catalogue results
    """
    # permission_classes = [IsAuthenticated, UserHasPerms]
    queryset = Dataset.objects.all().order_by('pk')
    serializer_class = GeoJSONSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (drf_filters.SearchFilter, filters.DjangoFilterBackend,)
    search_fields = ['title', 'abstract']
    filterset_fields = {
        'date':['gte','lte'],
        'category__identifier': ['exact'],
        'regions': ['exact'], 
    }


    def get_queryset(self):

        queryset = super(GeoJSONViewSet, self).get_queryset()

        # === FETCHING DATA ===
        queryset = Dataset.objects.all().filter(is_approved=True).exclude(subtype='remote')

        # GET parameters
        param_bbox = self.request.GET.get('bbox')

        # BBOX filter
        if param_bbox != None:
            #queryset = filter_bbox(queryset,param_bbox)
            param_bbox_coords = [float(x) for x in param_bbox.split(',')]
            shapely_geom = shapely_geometry.box(param_bbox_coords[0], param_bbox_coords[1], param_bbox_coords[2], param_bbox_coords[3])
            # shapely_switched_geom = shapely.ops.transform(lambda x, y: (y, x), shapely_geom)
            param_bbox_geom = shapely_geom.wkt
            queryset = queryset.filter(ll_bbox_polygon__intersects=param_bbox_geom).filter(ll_bbox_polygon__isvalid=True).exclude(ll_bbox_polygon__isnull=True)
            #queryset = queryset.filter(bbox_polygon__contained=param_bbox_geom).filter(bbox_polygon__isvalid=True).exclude(bbox_polygon__isnull=True)

        return queryset