from modeltranslation.translator import translator, TranslationOptions
from .models import TopicCategoryGDC


class TopicCategoryGDCTranslationOptions(TranslationOptions):
    fields = ()

translator.register(TopicCategoryGDC, TopicCategoryGDCTranslationOptions)