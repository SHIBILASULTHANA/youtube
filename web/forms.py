from django import forms
from .models import Channel,Video,Feedback

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        exclude = ('user',)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'thumbnail', 'channel', 'video_file','duration']
        
    def __init__(self, user, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = Channel.objects.filter(user=user)

    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']