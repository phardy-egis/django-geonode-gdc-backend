# Django base
from .serializers import *
from django.shortcuts import get_object_or_404
from geonode.layers.models import *
from geonode.base.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse, Http404
import shapely

# Models
from .models import TopicCategoryGDC

# Cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# Permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from geonode.base.api.permissions import (
    UserHasPerms,
)

# Tool to filter bbox
from geonode.base.bbox_utils import filter_bbox # filter_bbox(queryset, bbox) => BBOX as text "xmin,ymin,xmax,ymax"

class ResourceDetailCustomViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to filter geo-spatial data catalogue results
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticatedOrReadOnly, UserHasPerms]
    queryset = Dataset.objects.all()
    serializer_class = ResourceDetailSerializer

    @method_decorator(cache_page(60*5, cache='resources'))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, pk=None):
        queryset = self.queryset
        resource = get_object_or_404(queryset, pk=pk)
        serializer = ResourceDetailSerializer(resource)
        return Response(serializer.data)

def ResourceCustomListJSONView(request):
    
    #serializer_class = ResourceSerializer
    #authentication_classes = [SessionAuthentication, BasicAuthentication, OAuth2Authentication]
    #permission_classes = [IsAuthenticatedOrReadOnly, UserHasPerms]

    # === FETCHING DATA ===
    queryset = Dataset.objects.all().filter(is_approved=True).exclude(subtype='remote')

    # GET parameters
    param_bbox = request.GET.get('bbox')
    param_categories = request.GET.get('categories')
    param_search = request.GET.get('search')
    param_regions= request.GET.get('regions')
    param_date_begin= request.GET.get('date_begin')
    param_date_end= request.GET.get('date_end')

    # BBOX filter
    if param_bbox  != None and param_search != '':
        #queryset = filter_bbox(queryset,param_bbox)
        param_bbox_coords = [float(x) for x in param_bbox.split(',')]
        param_bbox_geom = shapely.geometry.box(param_bbox_coords[0], param_bbox_coords[1], param_bbox_coords[2], param_bbox_coords[3]).wkt
        queryset = queryset.filter(ll_bbox_polygon__intersects=param_bbox_geom).filter(ll_bbox_polygon__isvalid=True).exclude(ll_bbox_polygon__isnull=True)
        #queryset = queryset.filter(bbox_polygon__contained=param_bbox_geom).filter(bbox_polygon__isvalid=True).exclude(bbox_polygon__isnull=True)

    # Categories filter
    if param_categories != None and param_categories != '':
        param_categories = param_categories.split(',')
        queryset = queryset.filter(category__identifier__in = param_categories)
    
    # Research filter on "title"
    if param_search != None and param_search != '':
        param_search = param_search.split(' ')
        for keyword in param_search:
            queryset = queryset.filter(title__icontains=keyword)
    
    # Date filter
    if (param_date_begin != None and param_date_begin != '') and (param_date_end != None and param_date_end != '') :
        queryset = queryset.filter(date__gt=param_date_begin, date__lt=param_date_end)
    elif (param_date_begin != None and param_date_begin != ''):
        queryset = queryset.filter(date__gt=param_date_begin)
    elif (param_date_end != None and param_date_end != ''):
        queryset = queryset.filter(date__lt=param_date_end)

    # Region filter
    if param_regions != None and param_regions != '':
        param_regions = param_regions.split(',')
        print(param_regions)
        queryset = queryset.filter(regions__lft__gt=param_regions[0], regions__rght__lt=param_regions[1])



    geojson = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {'name': 'EPSG:4326'}
        },
        'features': []
    }

    for feature in queryset.all():
        if feature.ll_bbox_polygon is None:
            feature = {
                'type': 'Feature',
                'geometry': None,
                'properties': {
                    'pk': feature.pk
                }
            }
        else:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [feature.ll_bbox_polygon.coords[0]]
                },
                'properties': {
                    'pk': feature.pk
                }
            }
        geojson['features'].append(feature)
    
    return JsonResponse(geojson)

class TopicCategoryGDCViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that lists categories.
    """
    #authentication_classes = [SessionAuthentication, BasicAuthentication, OAuth2Authentication]
    #permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = TopicCategoryGDC.objects.all()
    serializer_class = TopicCategoryGDCSerializer

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        category = get_object_or_404(queryset, pk=pk)
        serializer = TopicCategoryGDCSerializer(category)
        return Response(serializer.data)

# View used to check if user is logged in
def UserAuthCheck(request):
    if(request.user.is_authenticated):
        geojson = {
            'msg':'User is logged in', 
            'logged_in':True,
        }
        return JsonResponse(geojson)
    else:
        raise Http404("User is not authenticated")
    