from django.shortcuts import render,redirect
from .models import Playlist,Song
from django.views import View
from .forms import PlaylistModelForm,SongModelForm

class PlaylistsView(View):
    template_name = 'songs/playlist.html'
    def get(self, request):
        playlists=Playlist.objects.filter(user=request.user)
        all_lists= []
        for playlist in playlists:
            all_lists.append(playlist)
        context= {'lists':all_lists}
        return render(request,self.template_name, context)

class PlaylistDetailView(View):
    template_name = 'songs/playlist_detail.html'
    def get(self, request, id):
        playlist = Playlist.objects.get(pk=id)
        qs= playlist.get_list()
        return render(request, self.template_name, {'qs': qs,'list':playlist})

def create_playlist(request):
    form = PlaylistModelForm()
    form.instance.user = request.user
    if request.method == "POST":
        form = PlaylistModelForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('/playlist/')
    context = {'form':form}
    return render(request,'songs/Playlist_form.html',context)

def delete_playlist(request,id):
    playlist = Playlist.objects.get(pk=id)
    playlist.delete()
    s = "/playlist/"
    return redirect(s)

def create_song(request,id):
    form = SongModelForm()
    playlist = Playlist.objects.get(pk=id)
    if request.method == "POST":
        temp = request.POST['form']
        obj = Song.objects.get(pk=temp)
        playlist.list.add(obj)
        s = "/playlist/" + str(id)+'/'
        return redirect(s)
    context = {'form':form}
    return render(request, 'songs/Song_form.html', context)

def play_song(request,id):
    song = Song.objects.get(pk=id)
    song_id= song.songid
    result = ("https://open.spotify.com/embed/track/" + song_id)
    return render(request, 'songs/play_song.html', {"result": result})

def delete_song(request,id, songid):
    playlist = Playlist.objects.get(pk=id)
    obj = Song.objects.get(pk=songid)
    playlist.list.remove(obj)
    s = "/playlist/" + str(id) + '/'
    return redirect(s)
