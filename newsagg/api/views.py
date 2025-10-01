from django.shortcuts import render
from rest_framework import generics
from aggregator.models import NewsItem


class NewsListAPIView(generics.ListAPIView):
    queryset = NewsItem.objects.all()

    def get_serializer_class(self):
        from .serializers import NewsItemSerializer
        return NewsItemSerializer


def empty_view(request):
    return render(request, 'api/empty.html')
