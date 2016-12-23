# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask_app.models import Question, QuestionLike, Answer, AnswerLike
from random import choice, randint


class Command(BaseCommand):
    def handle(self, *args, **options):
        questions = Question.objects.all()

        for q in questions:
            QuestionLike.objects.sum_for_question(q)
            q.save()

        answers = Answer.objects.all()

        for ans in answers:
            AnswerLike.objects.sum_for_answer(ans)
            ans.save()
