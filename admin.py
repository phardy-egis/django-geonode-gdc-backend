from django.contrib import admin
from .models import TopicCategoryGDC
from modeltranslation.admin import TabbedTranslationAdmin
from geonode import settings



class TopicCategoryAdminGDC(TabbedTranslationAdmin):
    model = TopicCategoryGDC
    list_display_links = ('identifier',)
    list_display = (
        'identifier',
        'description',
        'gn_description',
        'fa_class',
        'is_choice')
    if settings.MODIFY_TOPICCATEGORY is False:
        exclude = ('identifier', 'description',)

    def has_add_permission(self, request):
        # the records are from the standard TC 211 list, so no way to add
        if settings.MODIFY_TOPICCATEGORY:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        # the records are from the standard TC 211 list, so no way to remove
        if settings.MODIFY_TOPICCATEGORY:
            return True
        else:
            return False

admin.site.register(TopicCategoryGDC, TopicCategoryAdminGDC)