from django.core.management.base import BaseCommand
from main.models import GoogleFitMember
from open_humans.models import OpenHumansMember
from datauploader.tasks import fetch_googlefit_data
# from googlefit.settings import OPENHUMANS_CLIENT_ID, OPENHUMANS_CLIENT_SECRET
from django.conf import settings

class Command(BaseCommand):
    help = 'Import existing users from legacy project. Refresh (and save) OH/GoogleFit tokens for all members'

    def add_arguments(self, parser):
        parser.add_argument('--infile', type=str,
                            help='CSV with project_member_id & refresh_token')
        parser.add_argument('--delimiter', type=str,
                            help='CSV delimiter')

    def handle(self, *args, **options):
        for line in open(options['infile']):
            line = line.strip().split(options['delimiter'])
            oh_id = line[0]
            oh_refresh_token = line[1]
            moves_refresh_token = line[2]
            if len(OpenHumansMember.objects.filter(
                        oh_id=oh_id)) == 0:
                openhumansmember = OpenHumansMember.create(
                                    oh_id=oh_id,
                                    access_token="mock",
                                    refresh_token=oh_refresh_token,
                                    expires_in=-3600)
                openhumansmember.save()
                openhumansmember._refresh_tokens(client_id=settings.OPENHUMANS_CLIENT_ID,
                                            client_secret=settings.OPENHUMANS_CLIENT_SECRET)
                openhumansmember = OpenHumansMember.objects.get(oh_id=oh_id)
                print("made it to googlefitmember")
                googlefit_member = GoogleFitMember(
                    access_token="mock",
                    refresh_token=moves_refresh_token,
                    expires_in=GoogleFitMember.get_expiration(
                        -3600)
                )
                print(googlefit_member)
                googlefit_member.user = openhumansmember
                googlefit_member._refresh_tokens()
                # fetch_googlefit_data.delay(openhumansmember.oh_id, openhumansmember.googlefit_member.access_token)