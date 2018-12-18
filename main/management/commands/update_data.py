from django.core.management.base import BaseCommand
from main.models import GoogleFitMember
from open_humans.models import OpenHumansMember
from main.views import fetch_googlefit_data
from googlefit.settings import OPENHUMANS_CLIENT_ID, OPENHUMANS_CLIENT_SECRET
import arrow
from datetime import timedelta

class Command(BaseCommand):
    help = 'Update data for all users'

    def handle(self, *args, **options):
        googlefit_users = GoogleFitMember.objects.all()
        for user in googlefit_users:
            if user.last_updated < (arrow.now() - timedelta(days=4)):
                print("running update for user {}".format(user.userid))
                fetch_googlefit_data.delay(user.id, user.access_token)
            else:
                print("didn't update {}".format(user.userid))