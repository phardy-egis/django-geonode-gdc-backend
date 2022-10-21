from django.db import models
from geonode.base.models import TopicCategory

class TopicCategoryGDC(TopicCategory):
    
    # To order icons
    position_index = models.IntegerField(verbose_name='Position index',null=True, blank=True)

    # To allow adding images from admin interface
    icon_img = models.FileField(verbose_name='Image icon',null=True, blank=True)