from django.urls import path
from . import views
from .views import create_channel,channel_detailpage,upload_video,video_detailpage,subscribe,subscriptions,like_video,history,feedback,download_video

urlpatterns = [
    path("",views.index,name='index'),
    path('create_channel/', create_channel, name='create_channel'),
    path('upload-video/', upload_video, name='upload_video'),
    path('trending/',views.trending,name='trending'),
    path('channels/',views.channels,name='channels'),
    path('video_detailpage/<int:id>/', video_detailpage, name='video_detailpage'),
    path('channel/<int:id>/', channel_detailpage, name='channel_detailpage'),
    path('subscribe/<int:channel_id>/', subscribe, name='subscribe'),
    path('channel/<int:channel_id>/', channel_detailpage, name='channel_detailpage'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('liked_videos/<int:id>/like/', like_video, name='like_video'),
    path('liked_videos/',views.liked_videos, name='liked_videos'),
    path('history/', history, name='history'),
    path('feedback/', feedback, name='feedback'),
    path('download/<int:video_id>/', download_video, name='download_video'),
]