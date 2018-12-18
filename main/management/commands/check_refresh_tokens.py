from django.core.management.base import BaseCommand
from main.models import GoogleFitMember


class Command(BaseCommand):
    help = 'Update data for all users'

    def handle(self, *args, **options):
        for fb in GoogleFitMember.objects.all():
            print(fb.user.user.openhumansmember.oh_id)
            fb._refresh_tokens()
