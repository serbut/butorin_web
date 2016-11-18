# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from ask_app.models import Question, Tag

from random import choice, randint
import os

class Command(BaseCommand):
    help = 'Creates fake tags'

    def add_arguments(self, parser):
        parser.add_argument('--min',
                            action='store',
                            dest='min',
                            default=1,
                            )

        parser.add_argument('--max',
                            action='store',
                            dest='max',
                            default=3,
                            )

    def handle(self, *args, **options):
        tags = Tag.objects.all()
        for q in Question.objects.all():
            self.stdout.write('question [%d]... done' % q.id)
            for i in range(0, randint(int(options['min']), int(options['max']))):
                t = choice(tags)
                if t not in q.tags.all():
                    q.tags.add(t)
