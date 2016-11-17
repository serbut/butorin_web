# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask_app.models import Profile
from faker import Factory
import urllib
from django.core.files import File


class Command(BaseCommand):
    help = 'Generate users'

    def add_arguments(self, parser):
        parser.add_argument('-n',
                            action='store',
                            dest='number',
                            default=1,
                            )

    def handle(self, *args, **options):
        fake = Factory.create('ru_RU')

        number = int(options['number'])

        for i in range(0, number):
            profile = fake.simple_profile()

            u = User()
            u.username = profile['username']
            u.first_name = fake.first_name()
            u.last_name = fake.last_name()
            u.email = profile['mail']
            u.password = make_password('1234')
            u.is_active = True
            u.is_superuser = False
            u.save()

            up = Profile()
            up.user = u
            image_url = 'http://lorempixel.com/60/60/people'
            image_url = urllib.quote(image_url.encode('utf8'), ':/')
            content = urllib.urlretrieve(image_url)
            up.avatar.save('%s.png' % u.username, File(open(content[0])), save=True)
            up.save()

            self.stdout.write('added user %s' % u.username)