from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Channel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    channel_name = models.CharField(max_length=255)
    channel_profile = models.ImageField(upload_to='channel_profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.channel_name
 
class Video(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnail_picture/',null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    no_of_views = models.IntegerField(default=0)
    DURATION_CHOICES = [
        ('2 Days', '2 Days'),('few Days','few Days'),('3 Years','3 Years'),('6 Months', '6 Months'),
        ('1 Month','1 Month'),('4 Weeks','4 Weeks'),('6 Years', '6 Years'),('5 Hours','5 Hours')
    ]
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='2 Days')

    time = models.DateTimeField(auto_now_add=True) 
    likes = models.ManyToManyField(User, related_name='liked_videos')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.upload_date = timezone.now()
        super().save(*args, **kwargs)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return self.channel.channel_name

class LikedVideos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_videos = models.ManyToManyField(Video, related_name='users_who_liked')

class WatchedHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.title

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
