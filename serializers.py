from rest_framework import serializers
from geonode.base.models import ResourceBase
from .models import TopicCategoryGDC

class TopicCategoryGDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicCategoryGDC
        fields = '__all__'

class DetailsSerializer(serializers.ModelSerializer):
    #categories = TopicCategoryGDCSerializer(read_only=True)
    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='gn_description'
    )
    regions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = ResourceBase
        fields = ['title', 'thumbnail_url' , 'detail_url', 'alternate', 'date', 'date_type', 'raw_data_quality_statement', 'raw_supplemental_information', 'raw_abstract', 'alternate', 'regions', 'category', 'bbox_polygon','ll_bbox_polygon']

class GeoJSONSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['pk', 'title', 'abstract' ,'ll_bbox_polygon']

    def to_representation(self, obj):
        
        if len(obj.abstract) > 150:
            formated_abstract = obj.abstract[:150-3] + '...'
        else:
            formated_abstract = obj.abstract

        properties =  {
            'pk': obj.pk,
            'title': obj.title,
            'abstract': formated_abstract,
            'detail_url': obj.detail_url
        }

        geometry = None
        if obj.ll_bbox_polygon:
            geometry = {
                'type': 'Polygon',
                'coordinates': [obj.ll_bbox_polygon.coords[0]]
            },
        
        feature = {
            'type': 'Feature',
            'properties': properties,
            'geometry': geometry,
        }
        return feature
    
    class Meta:
        model = ResourceBase
        fields = ['title', 'thumbnail_url' , 'detail_url', 'alternate', 'date', 'date_type', 'raw_data_quality_statement', 'raw_supplemental_information', 'raw_abstract', 'alternate', 'regions', 'category', 'bbox_polygon','ll_bbox_polygon']
