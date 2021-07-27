from django.urls import path
from recommender import views

urlpatterns = [
path('', views.index, name='homepage'),
path('predictImage', views.predictImage, name='predictImage'),
path('song', views.song_playing, name='song'),
path('analysis', views.analysis, name='analysis'),
]

