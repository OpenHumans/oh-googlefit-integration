from django.core.management.base import BaseCommand
from main.models import GoogleFitMember
from open_humans.models import OpenHumansMember
from datauploader.tasks import fetch_googlefit_data
# from googlefit.settings import OPENHUMANS_CLIENT_ID, OPENHUMANS_CLIENT_SECRET
from django.conf import settings

class Command(BaseCommand):
    help = 'Refresh GoogleFit tokens that were previously broken'

    def add_arguments(self, parser):
        parser.add_argument('--infile', type=str,
                            help='CSV with project_member_id & refresh_token')
        parser.add_argument('--delimiter', type=str,
                            help='CSV delimiter')

    def handle(self, *args, **options):
        for line in open(options['infile']):
            if not line.startswith('proj_member_id'):
                line = line.strip().split(options['delimiter'])
                oh_id = line[0]
                oh_refresh_token = line[1]
                googlefit_refresh_token = line[2]
                if len(OpenHumansMember.objects.filter(
                            oh_id=oh_id)) == 1:
                    openhumansmember = OpenHumansMember.objects.get(oh_id=oh_id)
                    if hasattr(openhumansmember, 'googlefit_member'):
                        googlefit_member = openhumansmember.googlefit_member
                        print(googlefit_member)
                        successful_refresh = googlefit_member._refresh_tokens()
                        if not successful_refresh:
                            googlefit_member.refresh_token = googlefit_refresh_token
                            googlefit_member.save()
                            googlefit_member._refresh_tokens()
                    # fetch_googlefit_data.delay(openhumansmember.oh_id, openhumansmember.googlefit_member.access_token)
