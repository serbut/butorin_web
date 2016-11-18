# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


class QuestionManager(models.Manager):
    def quest_likes(self):
        q = self.annotate(answers=Count('answer__id', distinct=True))
        q = q.annotate(rating=Sum('questionlike__value'))
        return q

    def best(self):
        return self.quest_likes().order_by('-rating')

    def with_tag(self, tag):
        return self.quest_likes().filter(tags=tag).order_by('-date')

    def new(self):
        return self.quest_likes().order_by('-date')

    def single(self, id):
        q = self.quest_likes().get(pk=id)
        q.answers = Answer.objects.filter(question_id=id)
        q.answers.rating = q.answers.annotate(rating=Sum('answerlike__value'))
        return q


class AnswerManager(models.Manager):
    def ans_likes(self):
        a = self.annotate(rating=Sum('answerlike__value'))
        return a


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'Тэг')

    class Meta:
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'

    def __unicode__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    author = models.ForeignKey(User, verbose_name=u'Автор')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Дата и время')
    tags = models.ManyToManyField(Tag, verbose_name=u'Тэги')
    objects = QuestionManager()

    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(verbose_name=u'Текст')
    question = models.ForeignKey(Question, verbose_name=u'Вопрос')
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Дата и время')
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Ответ'
        verbose_name_plural = u'Ответы'

    def __unicode__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Пользователь')
    avatar = models.ImageField(upload_to='static/images/avatars', verbose_name=u'Аватар')

    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    def __unicode__(self):
        return str(self.user_id)


class QuestionLike(models.Model):
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=0)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=0)

