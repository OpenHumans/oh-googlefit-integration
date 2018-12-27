import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from datauploader.tasks import fetch_googlefit_data
from openhumans.models import OpenHumansMember


class Command(BaseCommand):
    help = 'Update data for all users'

    def handle(self, *args, **options):
        requests.get(settings.OPENHUMANS_APP_BASE_URL) # nudge asleep heroku instance to wake up :)
        users = OpenHumansMember.objects.all()
        for user in users:
            fetch_googlefit_data.delay(user.oh_id)
