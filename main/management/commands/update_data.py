from django.core.management.base import BaseCommand
from datauploader.tasks import fetch_googlefit_data
from openhumans.models import OpenHumansMember


class Command(BaseCommand):
    help = 'Update data for all users'

    def handle(self, *args, **options):
        users = OpenHumansMember.objects.all()
        for user in users:
            fetch_googlefit_data.delay(user.oh_id)
