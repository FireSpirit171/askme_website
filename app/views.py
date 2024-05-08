from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from app import models
from app.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User



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



def index(request):
    questions = models.Question.objects.get_new()
    page_obj = paginate(request, questions )
    if request.user.is_authenticated:
        return render(request, "index.html", {"questions": page_obj, "user": request.user})
    else:
        return render(request, "index.html", {"questions": page_obj})


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



def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Аутентификация пользователя
                return redirect(reverse('index'))
    else:
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form, "user": request.user})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            nickname = form.cleaned_data.get('nickname')
            avatar = form.cleaned_data.get('avatar')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken. Please choose another.')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                if avatar:  # Save avatar if uploaded
                    user.avatar = avatar
                    user.save()
                # Authenticate user after registration
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)  # Authenticate the user
                    return redirect('index')  # Redirect to the index page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})



def member( request, member_name ):
    user_profile = models.User_profile.objects.get_member(member_name)
    return render(request, "member.html", {"member": user_profile})


@login_required
def settings( request ):
    return render( request, "settings.html", {'user':request.user} )



def ask( request ):
    return render( request, "ask.html" )

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))