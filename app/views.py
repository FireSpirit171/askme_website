from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Question, Answer, Tag, User_profile, LikeQuestion, LikeAnswer
from app.forms import LoginForm, RegistrationForm, SettingsForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import json


def paginate(request, items, num_items=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(items, num_items)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj



def index(request):
    questions = Question.objects.get_new()
    page_obj = paginate(request, questions )
    if request.user.is_authenticated:
        user_profile = User_profile.objects.get(user = request.user)
        liked_questions = LikeQuestion.objects.filter(user=user_profile, status='l').values_list('question_id', flat=True)
        disliked_questions = LikeQuestion.objects.filter(user=user_profile, status='d').values_list('question_id', flat=True)
        return render(request, "index.html", {"questions": page_obj, "user": request.user, "user_profile": user_profile, 'liked_questions': liked_questions, 'disliked_questions': disliked_questions})
    else:
        return render(request, "index.html", {"questions": page_obj})


def hot( request ):
    questions = Question.objects.get_hot()
    page_obj = paginate(request, questions )
    if request.user.is_authenticated:
        user_profile = User_profile.objects.get(user = request.user)
        liked_questions = LikeQuestion.objects.filter(user=user_profile, status='l').values_list('question_id', flat=True)
        disliked_questions = LikeQuestion.objects.filter(user=user_profile, status='d').values_list('question_id', flat=True)
        return render(request, "hot.html", {"questions": page_obj, "user": request.user, "user_profile": user_profile, 'liked_questions': liked_questions, 'disliked_questions': disliked_questions})
    else:
        return render( request, "hot.html", {"questions": page_obj})


def tag( request, tag_name ):
    tag = get_object_or_404(Tag, name=tag_name) 
    questions = Question.objects.by_tag(tag_name)
    page_obj = paginate(request, questions )
    if request.user.is_authenticated:
        user_profile = User_profile.objects.get(user = request.user)
        liked_questions = LikeQuestion.objects.filter(user=user_profile, status='l').values_list('question_id', flat=True)
        disliked_questions = LikeQuestion.objects.filter(user=user_profile, status='d').values_list('question_id', flat=True)
        return render ( request, "tag.html", {"questions": page_obj, "tag": tag, "user": request.user, "user_profile": user_profile, 'liked_questions': liked_questions, 'disliked_questions': disliked_questions})
    else:
        return render ( request, "tag.html", {"questions": page_obj, "tag": tag})

def question(request, question_id):
    try:
        question = Question.objects.get_one_question(question_id)
        answers = Answer.objects.by_question(question_id)
        page_obj = paginate(request, answers)
        liked_answers = None
        disliked_answers = None
        if request.user.is_authenticated:
            liked_answers = LikeAnswer.objects.filter(user=request.user.user_profile, status='l').values_list('answer_id', flat=True)
            disliked_answers = LikeAnswer.objects.filter(user=request.user.user_profile, status='d').values_list('answer_id', flat=True)
        
        if request.user.is_authenticated:
            try:
                like_question = LikeQuestion.objects.get(user = request.user.user_profile, question = question)
            except:
                like_question = None

        if request.method == "POST" and request.user.is_authenticated:
            answer_text = request.POST.get('answer')
            if answer_text:
                question = get_object_or_404(Question, pk=question_id)
                user_profile = request.user.user_profile
                new_answer = Answer.objects.create(text=answer_text, author=user_profile, question=question)
                question.num_answers += 1
                question.save()
                
                # После создания ответа перенаправляем пользователя на страницу, на которой этот ответ будет отображаться
                updated_answers = Answer.objects.by_question(question_id)  # Получаем обновленный список ответов
                for index, answer in enumerate(updated_answers, start=1):
                    if answer.text == new_answer.text and answer.created_at == new_answer.created_at:
                        num_page = (index - 1) // page_obj.paginator.per_page + 1
                        return redirect(f"/questions/{question_id}?page={num_page}")
                
        return render(request, "question.html", {"question": question, 
                                                 "answers": page_obj, 
                                                 "user": request.user if request.user.is_authenticated else None,
                                                 'like_question': like_question if request.user.is_authenticated else None,
                                                 'liked_answers': liked_answers,
                                                 'disliked_answers': disliked_answers})
    except Question.DoesNotExist:
        return get_object_or_404(User_profile, question=question_id)



def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
    else:
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form, "user": request.user})

@transaction.atomic
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
                if not avatar:
                    avatar = 'default_user_icon.png'
                user = form.save()
                user_profile = User_profile.objects.create(user=user, nickname=nickname, avatar=avatar)

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


def member( request, member_name ):
    user_profile = User_profile.objects.get_member(member_name)
    return render(request, "member.html", {"member": user_profile})


@login_required
def settings(request):
    user = request.user
    user_profile = user.user_profile

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form_data = form.cleaned_data
            # Проверяем, были ли изменения в данных пользователя
            if user.username != form_data['username']:
                user.username = form_data['username']
            if user.email != form_data['email']:
                user.email = form_data['email']
            user.save()
            # Сохраняем профиль пользователя
            form.save()
            return redirect('settings')  # Перенаправление на страницу настроек после сохранения
        else:
            return render(request, "settings.html", {'user': user, 'user_profile': user_profile, 'form':form})
    else:
        return render(request, "settings.html", {'user': user, 'user_profile': user_profile})

@login_required
def ask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        tag_names = request.POST.get('tags')
        author_profile = request.user.user_profile
        tag_names_list = [name.strip() for name in tag_names.split(',')]

        tags = []
        for name in tag_names_list:
            tag, created = Tag.objects.get_or_create(name=name)
            if created:
                # Тег был только что создан, поэтому устанавливаем num_questions в 1
                tag.num_questions = 1
            else:
                # Тег уже существует, поэтому увеличиваем num_questions на 1
                tag.num_questions += 1
            tag.save()
            tags.append(tag)

        new_question = Question.objects.create(
            title=title,
            text=text,
            author=author_profile
        )
        new_question.tag.set(tags)
        return redirect('question', question_id=new_question.id)

    else:
        return render(request, 'ask.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@require_http_methods(["POST"])
def like_question(request, question_id):
    if request.method == 'POST':
        body = json.loads(request.body)
        action = body.get('action')
        question = get_object_or_404(Question, pk=question_id)
        user = request.user.user_profile

        if action == 'like':
            status = 'l'
        elif action == 'dislike':
            status = 'd'
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        like_question, created = LikeQuestion.objects.get_or_create(user=user, question=question)

        if created:
            user.activity += 1
            user.save()
        else:
            if like_question.status == status:
                like_question.delete()
                user.activity -= 1
                user.save()

                likes = question.likequestion_set.filter(status='l').count() - question.likequestion_set.filter(status='d').count()
                question.num_likes = likes
                question.save()
                return JsonResponse({'likes': likes, 'user_status': None})
        
        like_question.status = status
        like_question.save()

        likes = question.likequestion_set.filter(status='l').count() - question.likequestion_set.filter(status='d').count()
        question.num_likes = likes
        question.save()

        return JsonResponse({'likes': likes, 'user_status': status})

    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def like_answer(request, answer_id):
    if request.method == 'POST':
        body = json.loads(request.body)
        action = body.get('action')
        answer = get_object_or_404(Answer, pk=answer_id)
        user = request.user.user_profile

        if action == 'like':
            status = 'l'
        elif action == 'dislike':
            status = 'd'
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        like_answer, created = LikeAnswer.objects.get_or_create(user=user, answer=answer)

        if created:
            user.activity += 1
            user.save()
        else:
            if like_answer.status == status:
                like_answer.delete()
                user.activity -= 1
                user.save()

                likes = answer.likeanswer_set.filter(status='l').count() - answer.likeanswer_set.filter(status='d').count()
                answer.num_likes = likes
                answer.save()
                return JsonResponse({'likes': likes, 'user_status': None})
        
        like_answer.status = status
        like_answer.save()

        likes = answer.likeanswer_set.filter(status='l').count() - answer.likeanswer_set.filter(status='d').count()
        answer.num_likes = likes
        answer.save()

        return JsonResponse({'likes': likes, 'user_status': status})

    return JsonResponse({}, status=400)

@require_http_methods(["POST"])
def correct_answer(request, answer_id):
    if request.method == 'POST':
        body = json.loads(request.body)
        is_correct = body.get('is_correct')
        answer = get_object_or_404(Answer, pk=answer_id)
        user = request.user.user_profile  # Предположим, что у вас есть аутентифицированный пользователь
        
        # Проверяем, является ли пользователь автором вопроса
        if answer.question.author == user:
            answer.status = 'm' if is_correct else 'nm'
            answer.save()
            return JsonResponse({'status': answer.status})
        
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    return JsonResponse({}, status=400)