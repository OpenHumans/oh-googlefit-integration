from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember


class Command(BaseCommand):
    help = 'Delete data for user id'

    def add_arguments(self, parser):
        parser.add_argument('--ohid')

    def handle(self, *args, **options):
        users = OpenHumansMember.objects.all()
        for user in users:
            if user.oh_id == options['ohid']:
                user.delete_all_files()
