from rest_framework import serializers
from aggregator.models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ['id', 'title', 'summary', 'url', 'published_date', 'source']
