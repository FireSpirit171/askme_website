from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title" : f"Question {i}",
        "text": f" This is question number {i}",
        "tags": ['bla'*(i%4 + 1), 'be'*(i%3+1)],
        "author_id": i%50
    } for i in range(200)
]

ANSWERS = [
    {
        "text": f"Yes, I agree with you {i}",
        "question_id": i%100
    } for i in range(1000)
]

USERS = [
    {
        "id": i,
        "login": f"Member{i}",
        "nickname": f"chipichapa{i}"
    } for i in range(50)
]

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
    page_obj = paginate(request, QUESTIONS )
    return render( request, "index.html", {"questions": page_obj})

def hot( request ):
    questions = QUESTIONS[::-1]
    page_obj = paginate(request, questions )
    return render( request, "hot.html", {"questions": page_obj})

def tag( request, tag ):
    questions = [q for q in QUESTIONS if tag in q['tags']]
    page_obj = paginate(request, questions )
    return render ( request, "tag.html", {"questions": page_obj, "tag": tag})

def question( request, question_id ):
    question = QUESTIONS[question_id]
    answers = [answer for answer in ANSWERS if answer["question_id"]==question_id]
    return render( request, "question.html", {"question": question, "answers":answers})

def login( request ):
    return render( request, "login.html" )

def sighup( request ):
    return render( request, "signup.html" )

def member( request, member ):
    members = [u for u in USERS if u['nickname']==member]
    return render(request, "member.html", {"member": member} )

def settings( request ):
    return render( request, "settings.html" )

def ask( request ):
    return render( request, "ask.html" )