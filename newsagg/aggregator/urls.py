from django.urls import path
from . import views

urlpatterns = [
    path("", views.news_list, name="news_list"),
    path("news/<int:pk>/", views.news_detail_card, name="news_detail_card"),
]