from rest_framework import serializers
from geonode.base.models import ResourceBase
from .models import TopicCategoryGDC

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceBase
        fields = ['pk']

class TopicCategoryGDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicCategoryGDC
        fields = '__all__'

class ResourceDetailSerializer(serializers.ModelSerializer):
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