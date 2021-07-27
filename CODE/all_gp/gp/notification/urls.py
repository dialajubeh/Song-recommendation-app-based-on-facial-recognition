from django.urls import path
from notification import views

urlpatterns = [
path('<int:id>/', views.post, name="room"),
path('notifications/', views.notifications, name="notifications"),
path('delete_notification/<int:id>/', views.delete_notification, name='delete_notification'),
]