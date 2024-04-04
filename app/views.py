from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title" : f"Question {i}",
        "text": f" This is question number {i}"
    } for i in range(100)
]

ANSWERS = [
    {
        "text": f"Yes, I agree with you {i}",
        "question_id": i%100
    } for i in range(1000)
]

def index( request ):
    page_num = request.GET.get( 'page', 1 )
    paginator = Paginator( QUESTIONS, 5 )
    page_obj = paginator.page( page_num )
    return render( request, "index.html", {"questions": page_obj})

def hot( request ):
    questions = QUESTIONS[::-1]
    page_num = request.GET.get( 'page', 1 )
    paginator = Paginator( questions, 5 )
    page_obj = paginator.page( page_num )
    return render( request, "hot.html", {"questions": page_obj})

def tag( request ):
    questions = QUESTIONS[4:7]
    return render ( request, "tag.html", {"questions": questions})

def question( request, question_id ):
    question = QUESTIONS[question_id]
    answers = [answer for answer in ANSWERS if answer["question_id"]==question_id]
    return render( request, "question.html", {"question": question, "answers":answers})
