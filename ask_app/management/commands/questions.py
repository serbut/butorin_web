# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from random import choice, randint
from faker import Factory
from django.contrib.auth.models import User
from ask_app.models import Question


class Command(BaseCommand):
    help = 'Generate questions'

    def add_arguments(self, parser):
        parser.add_argument('-n',
                action='store',
                dest='number',
                default=1,
        )

    def handle(self, *args, **options):
        fake = Factory.create('ru_RU')
        number = int(options['number'])
        users = User.objects.all()

        for i in range(0, number):
            q = Question()
            q.title = fake.sentence(nb_words=randint(2, 8), variable_nb_words=True)
            q.text = u"%s" % (
                    fake.paragraph(nb_sentences=randint(5, 15), variable_nb_sentences=True),
                    )
            q.author = choice(users)
            q.save()
            self.stdout.write('created question [%d]' % q.id)
