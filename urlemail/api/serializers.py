from rest_framework import serializers
from urlemail.models import Actions
# from django.core.validators import URLValidator
# from django.core.exceptions import ValidationError


class ActionSerializer(serializers.ModelSerializer):

    urls = serializers.ListField(child=serializers.URLField())

    class Meta:
        model = Actions
        fields = ['pk', 'urls', 'email', 'timestamp']

    # def validate_urls(self, value):
    #     val = URLValidator()
    #     list_urls = value.strip().split(',')
    #     for url in list_urls:
    #         try:
    #             val(url)
    #         except ValidationError:
    #             raise serializers.ValidationError(url + "is not a url")
    #     return value
