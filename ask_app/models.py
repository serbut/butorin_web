# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


class AnswerManager(models.Manager):
    def ans_list(self, id):
        answers = self.filter(question_id=id).annotate(rating=Sum('answerlike__value'))
        return answers


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
        q.answers = Answer.objects.ans_list(id)
        return q


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name=u'Тэг')

    class Meta:
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'

    def __unicode__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    author = models.ForeignKey(User, verbose_name=u'Автор')
    date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата и время')
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
    author = models.ForeignKey(User, verbose_name=u'Пользователь')
    date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата и время')
    correct = models.BooleanField(default=False, verbose_name=u'Правильный ответ')
    objects = AnswerManager()

    class Meta:
        verbose_name = u'Ответ'
        verbose_name_plural = u'Ответы'

    def __unicode__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Пользователь')
    avatar = models.ImageField(upload_to='images/avatars', verbose_name=u'Аватар')

    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    def __unicode__(self):
        return str(self.user_id)


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, verbose_name=u'Вопрос')
    author = models.ForeignKey(User, verbose_name=u'Автор')
    value = models.SmallIntegerField(default=0, verbose_name=u'Значение')

    class Meta:
        verbose_name = u'Лайк вопроса'
        verbose_name_plural = u'Лайки вопросов'
        unique_together = ('author', 'question',)

    def __unicode__(self):
        return self.value


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, verbose_name=u'Ответ')
    author = models.ForeignKey(User, verbose_name=u'Автор')
    value = models.SmallIntegerField(default=0, verbose_name=u'Значение')

    class Meta:
        verbose_name = u'Лайк ответа'
        verbose_name_plural = u'Лайки ответов'
        unique_together = ('author', 'answer',)

    def __unicode__(self):
        return self.value

