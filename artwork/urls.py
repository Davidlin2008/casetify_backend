from django.urls import path 

from .views import RegularArtworkListView
from .views import HahaView


urlpatterns = [
    path('/regular/list', RegularArtworkListView.as_view()),
    path('/haha', HahaView.as_view()),
]
