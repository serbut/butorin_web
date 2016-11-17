# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask_app.models import Question, Answer
from random import choice, randint
from faker import Factory


class Command(BaseCommand):
    help = 'Generate answers'

    def add_arguments(self, parser):
        parser.add_argument('--min',
                            action='store',
                            dest='min',
                            default=1,
                            )
        parser.add_argument('--max',
                            action='store',
                            dest='max',
                            default=15,
                            )

    def handle(self, *args, **options):
        fake = Factory.create('ru_RU')
        users = User.objects.all()
        questions = Question.objects.all()

        for question in questions:
            for item in range(0, randint(int(options['min']), int(options['max']))):
                answer = Answer()
                answer.text = fake.paragraph(nb_sentences=randint(3, 8), variable_nb_sentences=True)
                answer.user = choice(users)
                answer.question = question
                answer.save()
                self.stdout.write('[%d] ans[%d]' % (question.id, answer.id))