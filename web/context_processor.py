from web.models import Channel

def main_context(request):
    is_create_channer = False
    if request.user.is_authenticated:
        if  Channel.objects.filter(user=request.user).exists():
            is_create_channer =True
    return{
        'is_create_channer':is_create_channer
    }