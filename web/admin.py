from django.contrib import admin
from .models import Channel,Video,Subscription,WatchedHistory,Feedback

# Register your models here.
admin.site.register(Channel)
admin.site.register(Video)
admin.site.register(Subscription)
admin.site.register(WatchedHistory)
admin.site.register(Feedback)