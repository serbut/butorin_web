# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from ask_app.models import Question, Answer, Profile
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Логин'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=u'Пароль'
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('username', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user

        else:
            raise forms.ValidationError(u'Неправильная пара логин/пароль!')


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', ]

    def __init__(self, author, *args, **kwargs):
        super(NewQuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'rows': 7,
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control'
        })
        self.author = author

    def save(self, commit=True):
        question = super(NewQuestionForm, self).save(commit=False)
        question.author = self.author
        if commit:
            question.save()
        return question.id


class NewAnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш ответ здесь', 'rows': 5}),
        max_length=100,
        label=u'Текст'
    )

    def save(self, author, question):
        data = self.cleaned_data
        a = Answer.objects.create(text=data.get('text'), author=author, question=question)
        a.save()
        return a


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Логин'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Имя'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Фамилия'
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'E-mail'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=u'Пароль'
    )
    password_check = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=u'Повторите пароль'
    )
    avatar = forms.FileField(
        widget=forms.ClearableFileInput(attrs={}),
        label=u'Аватар',
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError(u'Пользователь с таким логином уже существует')
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        p1 = self.cleaned_data.get('password', '')
        p2 = self.cleaned_data.get('password_check', '')

        if p1 != p2:
            raise forms.ValidationError(u'Введенные пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        profile = Profile()
        profile.user = u
        if data.get('avatar') is not None:
            avatar = data.get('avatar')
            profile.avatar.save('%s.png' % u.username, avatar, save=True)

        profile.save()

        return authenticate(username=u.username, password=password)


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Имя'
    )
    last_name = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Фамилия'
    )
    email = forms.EmailField(
        widget=forms.TextInput( attrs={'class': 'form-control'}),
        max_length=100,
        label=u'E-mail'
    )
    avatar = forms.FileField(
        widget=forms.ClearableFileInput(attrs={}),
        label=u'Аватар',
        required=False
    )

    def save(self, user):
        data = self.cleaned_data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        user.save()

        profile = user.profile
        profile.info = data.get('info')

        if data.get('avatar') is not None:
            avatar = data.get('avatar')
            profile.avatar.save('%s.png' % user.username, avatar, save=True)

        profile.save()
        return self


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=u'Новый пароль',
    )
    password_check = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=u'Повторите пароль',
    )

    def clean_password2(self):
        p1 = self.cleaned_data.get('password', '')
        p2 = self.cleaned_data.get('password_check', '')

        if p1 != p2:
            raise forms.ValidationError(u'Введенные пароли не совпадают')

    def save(self, user):
        p = self.cleaned_data.get('password', '')
        if p != '':
            user.set_password(p)

        user.save()
        return self

