# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count



class QuestionQuerySet(models.QuerySet):
    def tags(self):
        return self.prefetch_related('tags')

    def answers_count(self):
        return self.annotate(answers=Count('answer__id'))


class QuestionManager(models.Manager):
    def best(self):
        #============to fix==============
        return self.order_by('-date')

    def new(self):
        return QuestionQuerySet(self.model, using=self._db).tags().answers_count().order_by('-date')

    def single(self, id):
        q = self.get(pk=id)
        q.answers = Answer.objects.filter(question_id=id)
        #q.tags = Tag.objects.filter(question_id=id)
        return q



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
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag)
    #rating = models.IntegerField(default=0)
    objects = QuestionManager()
    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'

    def __unicode__(self):
        return self.title



class Answer(models.Model):
    text = models.TextField(verbose_name=u'Текст')
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.datetime.now)
    correct = models.BooleanField(default=False)
    class Meta:
        verbose_name = u'Ответ'
        verbose_name_plural = u'Ответы'

    def __unicode__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User)
    username = User.objects.first().username
    avatar = models.ImageField(upload_to='static/images/avatars')

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