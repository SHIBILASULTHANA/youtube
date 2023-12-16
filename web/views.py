from django.http import HttpResponse,FileResponse
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ChannelForm,VideoForm,FeedbackForm
from .models import Channel,Video,Subscription,LikedVideos,WatchedHistory
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

def index(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request,'web/index.html',context)

def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return redirect('channels')
    else:
        context = {
           "form" :   ChannelForm()
        }

    return render(request, 'web/create_channel.html', context)

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = VideoForm(user=request.user)

    return render(request, 'web/upload_video.html', {'form': form})

def channels(request):
    all_channels = Channel.objects.all()
    context = {'all_channels': all_channels}
    return render(request,'web/channels.html',context)

def channel_detailpage(request, id):
    channel = get_object_or_404(Channel, id=id)
    videos = Video.objects.filter(channel=channel)
    user_subscribed = False
    if request.user.is_authenticated:
        user_subscribed = Subscription.objects.filter(user=request.user, channel=channel).exists()

    context = {
        'channel': channel,
        'videos': videos,
        'user_subscribed': user_subscribed
        }
    return render(request, 'web/channel_detailpage.html', context)

@login_required
def video_detailpage(request, id):
    videos = get_object_or_404(Video, id=id)
    watched_entries = WatchedHistory.objects.filter(user=request.user, video=videos)

    if watched_entries.exists():
        watched_entry = watched_entries.first()
        watched_entry.watched_at = timezone.now()
        watched_entry.save()
    else:
        WatchedHistory.objects.create(user=request.user, video=videos)
    
    videos.no_of_views += 1
    videos.save()

    context = {'video': videos}
    return render(request, 'web/video_detailpage.html', context)

def trending(request):
    latest_videos = Video.objects.order_by('-time')[:6]
    return render(request, 'web/trending.html', {'latest_videos': latest_videos})

def subscribe(request, channel_id):
    if request.user.is_authenticated:
        channel = get_object_or_404(Channel, id=channel_id)
        subscription, created = Subscription.objects.get_or_create(user=request.user, channel=channel)

        if not created:
            subscription.delete()
            alert_message = f"Unsubscribed"
            return HttpResponse(f"<script>alert('{alert_message}'); window.location.href='/';</script>")
           
    return redirect('channel_detailpage', channel_id=channel_id) 

@login_required
def subscriptions(request):
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(user=request.user)
        return render(request, 'web/subscriptions.html', {'subscriptions': user_subscriptions})
    else:
        return redirect('login')

def like_video(request, id):
    videos = get_object_or_404(Video, id=id)
    liked_videos_instance, created = LikedVideos.objects.get_or_create(user=request.user)
    
    print(f'Video: {videos.title}, User: {request.user.username}, Likes: {videos.likes.all()}')

    if request.user in videos.likes.all():
        videos.likes.remove(request.user)
        liked_videos_instance.liked_videos.remove(videos)
    else:
        videos.likes.add(request.user)
        liked_videos_instance.liked_videos.add(videos)

    print(f'After: Likes: {videos.likes.all()}, Liked Videos: {liked_videos_instance.liked_videos.all()}')

    return redirect('video_detailpage', id=id)

@login_required
def liked_videos(request):
    try:
        liked_videos_instance = LikedVideos.objects.get(user=request.user)
        liked_videos = liked_videos_instance.liked_videos.all()
        print('liked_videos=',liked_videos)
    except LikedVideos.DoesNotExist:
        liked_videos = []

    return render(request, 'web/liked_videos.html', {'liked_videos': liked_videos})

@login_required
def history(request):
    watched_videos = WatchedHistory.objects.filter(user=request.user).order_by('-watched_at')
    context = {'watched_videos': watched_videos}
    return render(request, 'web/history.html', context)

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            alert_message = f"Feedback Submitted Successfully, Thank you {name}"
            return HttpResponse(f"<script>alert('{alert_message}'); window.location.href='/';</script>")
    else:
        form = FeedbackForm()

    return render(request, 'web/feedback.html', {'form': form})

def download_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    response = FileResponse(video.video_file, as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{video.title}.mp4"'

    return response