from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from ask_app.models import Profile
import urllib
from django.core.files import File


class Command(BaseCommand):
    help = 'Creates fake tags'

    def handle(self, *args, **options):
        users = User.objects.all()
        for u in users:
            profile = Profile()
            profile.user = u
            image_url = 'http://lorempixel.com/60/60/people'
            image_url = urllib.quote(image_url.encode('utf8'), ':/')
            content = urllib.urlretrieve(image_url)
            profile.avatar.save('%s.png' % u.username, File(open(content[0])), save=True)
            profile.save()
            self.stdout.write('avatar for user [%d]... done' % u.id)
