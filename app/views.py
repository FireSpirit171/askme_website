from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from app import models


# Create your views here.

def paginate(request, items, num_items=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(items, num_items)
    
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # Если параметр page не является целым числом, вернуть первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если параметр page превышает максимальное количество страниц, вернуть последнюю страницу
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

def index( request ):
    questions = models.Question.objects.get_new()
    page_obj = paginate(request, questions )
    return render( request, "index.html", {"questions": page_obj})

def hot( request ):
    questions = models.Question.objects.get_hot()
    page_obj = paginate(request, questions )
    return render( request, "hot.html", {"questions": page_obj})

def tag( request, tag_name ):
    tag = get_object_or_404(models.Tag, name=tag_name) 
    questions = models.Question.objects.by_tag(tag_name).annotate(num_likes=Count('likequestion'))
    page_obj = paginate(request, questions )
    return render ( request, "tag.html", {"questions": page_obj, "tag": tag})

def question( request, question_id ):
    try:
        question = models.Question.objects.annotate(num_likes=Count('likequestion')).get(id = question_id)
        answers = models.Answer.objects.by_question(question_id)
    except models.Question.DoesNotExist:
        return get_object_or_404(models.User_profile, question=question_id)
    return render( request, "question.html", {"question": question, "answers":answers})

def login( request ):
    return render( request, "login.html", {} )

def sighup( request ):
    return render( request, "signup.html", {} )

def member( request, member_name ):
    try:
        user_profile = models.User_profile.objects.annotate(num_likes=Count('likequestion', distinct=True) + Count('likeanswer', distinct=True)).get(nickname=member_name)
    except models.User_profile.DoesNotExist:
        return get_object_or_404(models.User_profile, nickname=member_name)
    return render(request, "member.html", {"member": user_profile})

def settings( request ):
    return render( request, "settings.html" )

def ask( request ):
    return render( request, "ask.html" )