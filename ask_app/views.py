from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ask_app.models import QuestionManager, Question, Answer, Tag

from django.http import HttpResponse, Http404



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
    questions = Question.objects.best()
    pagination = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': pagination,
        'type': 'hot',
    })


def tag(request, tag):
    try:
        tag = Tag.objects.get(title=tag)
    except Tag.DoesNotExist:
        raise Http404()
    questions = Question.objects.with_tag(tag)
    pagination = paginate(questions, request)
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
