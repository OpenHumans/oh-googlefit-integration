from ohapi import api
from django.conf import settings
import arrow
from datetime import timedelta

def get_googlefit_file(openhumansmember):
    try:
        oh_access_token = openhumansmember.get_access_token(
                                client_id=settings.OPENHUMANS_CLIENT_ID,
                                client_secret=settings.OPENHUMANS_CLIENT_SECRET)
        user_object = api.exchange_oauth2_member(oh_access_token)
        for dfile in user_object['data']:
            if 'GoogleFit' in dfile['metadata']['tags']:
                return dfile['download_url']
        return ''

    except:
        return 'error'


def can_update_data(googlefit_member):
    if not googlefit_member.last_submitted_for_update or googlefit_member.last_submitted_for_update < (arrow.now() - timedelta(hours=1)):
        return True
    return False