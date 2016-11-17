from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint, sample
from ask_app.models import QuestionManager, Question, Answer, Tag

from django.http import HttpResponse, Http404

#questions = []

#for i in range(1, 50):
#    questions.append({
#        'id': i,
#        'title': 'title ' + str(i),
#        'text': 'text ' + str(i),
#        'answers': randint(0, 25),
#        'rating': randint(-9, 9),
#        'tags': sample(['php', 'c++', 'django', 'python', 'mailru'], randint(1, 3)),
#    })




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

def index(request):
    questions = Question.objects.new()
    pagination = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': pagination,
        'type': 'all',
    })


def hot(request):
    questions = Question.objects.hot()
    pagination = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': pagination,
        'type': 'hot',
    })

def tag(request, tag):
    ################
    questions = Question.objects.new()
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
    try:
        q = Question.objects.single(id)
    except Question.DoesNotExist:
        raise Http404

    pagination = paginate(q.answers, request)
    return render(request, 'question.html', {
        'question': q,
        'answers': pagination,
        })

def signup(request):
    return render(request, 'signup.html', {})

def settings(request):
    return render(request, 'settings.html', {})