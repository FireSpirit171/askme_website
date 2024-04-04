from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "title" : f"Question {i}",
        "text": f" This is question number {i}"
    } for i in range(10)
]

ANSWERS = [
    {
        "text": f"Yes, I agree with you {i}",
        "question_id": i%10
    } for i in range(100)
]

def index( request ):
    return render( request, "index.html", {"questions": QUESTIONS})

def hot( request ):
    questions = QUESTIONS[::-1]
    return render( request, "hot.html", {"questions": questions})

def tag( request ):
    questions = QUESTIONS[4:7]
    return render ( request, "tag.html", {"questions": questions})

def question( request, question_id ):
    question = QUESTIONS[question_id]
    answers = [answer for answer in ANSWERS if answer["question_id"]==question_id]
    return render( request, "question.html", {"question": question, "answers":answers})
