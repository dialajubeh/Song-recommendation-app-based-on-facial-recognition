from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("homepage/", views.home_view, name="profile page"),
    path("myprofile/", views.my_profile_view, name="profile page"),
    path("invites/", views.invites_received_view, name="my-invites-view"),
    path("all-profiles/", views.ProfileListView.as_view(), name="all profiles view"),
    path("send-invite/", views.send_invatation, name="send-invite"),
    path("remove-friend/", views.remove_from_friends, name="remove-friend"),
    path("my-invites/accept/", views.accept_invitation, name="accept-invite"),
    path("my-invites/reject/", views.reject_invitation, name="reject-invite"),
    path("friends/", views.friends_view, name="friends view"),

]