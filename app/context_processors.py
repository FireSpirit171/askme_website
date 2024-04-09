from django.db.models import Count
from app.models import User_profile, Tag

def get_best_members(request):
    best_members = User_profile.objects.annotate(
        activity=Count('likequestion', distinct=True) + Count('likeanswer', distinct=True)
    ).order_by('-activity')[:5]
    return {'best_members': best_members}

def get_popular_tags(request):
    popular_tags = Tag.objects.annotate(
        num_questions = Count('question')
    ).order_by('-num_questions')[:8]
    return {'popular_tags': popular_tags}