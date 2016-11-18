# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask_app.models import Question, QuestionLike, Answer, AnswerLike
from random import choice, randint


class Command(BaseCommand):
    help = 'Generate likes'

    def add_arguments(self, parser):
        parser.add_argument('--likes-for-answers',
                action='store',
                dest='number_likes_answers',
                default=5,
        )
        parser.add_argument('--likes-for-questions',
                action='store',
                dest='number_likes_questions',
                default=5,
        )

    def handle(self, *args, **options):
        number_likes_answers = int(options['number_likes_answers'])
        number_likes_questions = int(options['number_likes_questions'])

        users = User.objects.all()
        questions = Question.objects.all()

        for q in questions:
            self.stdout.write('question [%d]' % q.id)
            for i in range(0, number_likes_questions):
                like = QuestionLike()
                like.author = choice(users)
                like.question = q
                like.value = choice([-1, 1])
                like.save()

        answers = Answer.objects.all()

        for ans in answers:
            self.stdout.write('answer [%d]' % ans.id)
            for i in range(0, number_likes_answers):
                like = AnswerLike()
                like.author = choice(users)
                like.answer = ans
                like.value = choice([-1, 1])
                like.save()
