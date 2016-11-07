from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint, sample

from django.http import HttpResponse

questions = []

for i in range(1, 150):
    questions.append({
        'id': i,
        'title': 'title ' + str(i),
        'text': 'text ' + str(i),
        'answers': randint(0, 25),
        'rating': randint(-9, 9),
        'tags': sample(['php', 'c++', 'django', 'python', 'mailru'], randint(1, 3)),
    })


def paginate(objects, request):

    page = request.GET.get('page')
    p = Paginator(objects, 10)

    try:
        result = p.page(page)
    except PageNotAnInteger:
        result = p.page(1)
    except EmptyPage:
        result = p.page(1)
    return result


def get_params(request):
        return render(request, 'get_params.html', {})

def index(request):
    pagination = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': pagination,
        'type': 'all',
    })

def hot(request):
    pagination = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': pagination,
        'type': 'hot',
    })

def tag(request, tag):
    questions_tag = []
    for question in questions:
        if str(tag) in question.get('tags'):
            questions_tag.append(question)

    pagination = paginate(questions_tag, request)
    return render(request,  'index.html', {
        'questions': pagination,
        'tag': tag,
        'type': 'tag',
    })

def ask(request):
    return render(request, 'ask.html', {})

def login(request):
    return render(request, 'login.html', {})

def question(request, id):
    id = int(id)
    answ = []
    for i in range(1, questions[id - 1].get('answers') + 1):
        answ.append({
            'text': 'answer ' + str(i) + ' for question ' + str(id),
            'rating': randint(-9, 9),
        })
    pagination = paginate(answ, request)
    q = {
        'id': id,
        'title': questions[id - 1].get('title'),
        'text': questions[id - 1].get('text'),
        'rating': questions[id - 1].get('rating'),
        'tags': questions[id - 1].get('tags'),
        'answers': pagination,
    }

    return render(request, 'question.html', q)

def signup(request):
    return render(request, 'signup.html', {})

def settings(request):
    return render(request, 'settings.html', {})