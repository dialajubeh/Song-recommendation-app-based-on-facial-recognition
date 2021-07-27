from django.shortcuts import render,redirect
from .models import Message, Message_received
from songs.models import Song
from notification.forms import FriendsModelForm
from django.views.generic import View
from django.contrib.auth.models import User
from profiles.models import Profile

def post(request, id):
    song = Song.objects.get(pk=id)
    sender_msg = request.user
    form = FriendsModelForm()
    user = request.user
    qs = Profile.get_friends(user)
    if request.method == "POST":
        form = FriendsModelForm(request.POST)
        if form.is_valid():
            rec = form.cleaned_data.get("receiver_msg")
            rec_obj = User.objects.get(username=rec)
            msg_instance = Message( sender_msg = sender_msg,receiver_msg = rec ,message_file =song)
            msg_instance.save()
            msg_received_instance = Message_received(sender=sender_msg.username, receiver = rec_obj,message_file =song)
            msg_received_instance.save()
            return render(request, 'profiles/myprofile.html')

    return render(request, 'notification/room.html', {'song':song,'form':form,"sender_msg":sender_msg,"qs":qs})

def notifications(request):
    all_msgs = Message_received.objects.filter(receiver=request.user)
    list_msgs={}
    for msg in all_msgs:
        msg_id = msg.message_file.songid
        song_msg = ("https://open.spotify.com/embed/track/" + msg_id)
        list_msgs[msg.sender] =[]
        list_msgs[msg.sender].append(song_msg)
        list_msgs[msg.sender].append(msg)
    print(list_msgs)
    context= {'list_msgs':list_msgs}
    return render(request, 'notification/msg_rec.html', context)
def delete_notification(request, id):
    message = Message_received.objects.get(pk=id)
    message.delete()
    return redirect('/room/notifications/')
