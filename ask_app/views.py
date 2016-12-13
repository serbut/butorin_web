from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ask_app.models import Question, Tag
from django.forms.models import model_to_dict
from ask_app.forms import SignupForm, NewQuestionForm, LoginForm, NewAnswerForm, ProfileForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse


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


@login_required
def ask(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.user, request.POST)
        if form.is_valid():
            q = form.save(request.user)
            return redirect(reverse('question', kwargs={'id': q}))
    else:
        form = NewQuestionForm(request.user)

    return render(request, 'ask.html', {'form': form})


def login(request):
    redirect_to = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            if redirect_to:
                return redirect(redirect_to)
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    redirect_to = request.GET.get('next')
    auth.logout(request)
    if redirect_to:
        return redirect(redirect_to)
    return redirect('/')


def question(request, id):
    try:
        q = Question.objects.single(id)
    except Question.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = NewAnswerForm(request.POST)
        if form.is_valid():
            form.save(request.user, q)
    else:
        form = NewAnswerForm()

    pagination = paginate(q.answers, request)
    return render(request, 'question.html', {
        'form': form,
        'question': q,
        'answers': pagination,
        })


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            auth.login(request, u)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
    else:
        user = model_to_dict(request.user)
        form = ProfileForm(user)

    return render(request, 'settings.html', {
        'type': 'profile',
        'form': form,
        'user': request.user,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            form.save(request.user)
    else:
        form = ChangePasswordForm()

    return render(request, 'settings.html', {
        'type': 'change_password',
        'form': form,
        'user': request.user,
    })
