from django.urls import path
from . import views
from django.conf.urls import url
from .views import PlaylistsView, PlaylistDetailView

urlpatterns = [
    #path("", views.playlists_view, name="profile page"),
    #path('<str:list_name>/', views.playlists_songs_view, name='playlist_song'),
    path('', PlaylistsView.as_view(), name='playlists'),
    path('<int:id>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('create_playlist', views.create_playlist, name='create_playlist'),
    path('<int:id>/create_song/', views.create_song, name='create_song'),
    path('play_song/<int:id>/', views.play_song, name='play_song'),
    path('delete_song/<int:id>/<int:songid>/', views.delete_song, name='delete_song'),
    path('delete_playlist/<int:id>/', views.delete_playlist, name='delete_playlist'),
]

