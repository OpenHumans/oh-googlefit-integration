from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember
from ohapi import api


class Command(BaseCommand):
    help = 'View metadata for data uploaded/synced'

    def handle(self, *args, **options):
        users = OpenHumansMember.objects.all()
        for user in users:
            try:
                member = api.exchange_oauth2_member(user.get_access_token())
            except:
                pass
            for dfile in member['data']:
                if 'GoogleFit' in dfile['metadata']['tags']:
                    print(dfile)
