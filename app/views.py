from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout as logOut
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from app import models
from app.forms import LoginForm


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
    questions = models.Question.objects.by_tag(tag_name)
    page_obj = paginate(request, questions )
    return render ( request, "tag.html", {"questions": page_obj, "tag": tag})



def question(request, question_id):
    try:
        question = models.Question.objects.get_one_question(question_id)
        answers = models.Answer.objects.by_question(question_id)
        page_obj = paginate( request, answers )
    except models.Question.DoesNotExist:
        return get_object_or_404(models.User_profile, question=question_id)
    return render( request, "question.html", {"question": question, "answers":page_obj})



def login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return redirect(reverse('index'))
    else:
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form})


def sighup( request ):
    return render( request, "signup.html", {} )



def member( request, member_name ):
    user_profile = models.User_profile.objects.get_member(member_name)
    return render(request, "member.html", {"member": user_profile})



def settings( request ):
    return render( request, "settings.html" )



def ask( request ):
    return render( request, "ask.html" )

def logout(request):
    logOut(request)
    return redirect(reverse('login'))