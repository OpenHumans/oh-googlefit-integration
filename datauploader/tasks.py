"""
Asynchronous tasks that update data in Open Humans.
These tasks:
  1. delete any current files in OH if they match the planned upload filename
  2. adds a data file
"""
import logging

import arrow
from celery import shared_task

from openhumans.models import OpenHumansMember
from datetime import datetime
from ohapi import api

from .googlefit_api import get_googlefit_data


# Set up logging.
logger = logging.getLogger(__name__)


def create_metadata(month):
    return {
        'description':
            'Google Fit data.',
        'tags': ['Google Fit', 'GoogleFit', 'activity', 'steps', 'calories', 'distance'],
        'updated_at': str(datetime.utcnow()),
        'month': month,
    }


@shared_task
def fetch_googlefit_data(oh_id):
    '''
    Fetches all of the googlefit data for a given user
    '''
    current_dt = datetime.utcnow()
    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
    gf_member = oh_member.googlefit_member
    oh_access_token = oh_member.get_access_token()
    gf_access_token = gf_member.get_access_token()

    filesmonth = get_googlefit_data(oh_access_token, gf_access_token, current_dt)
    for fn, month in filesmonth:
        #TODO: replace if already exists :-)
        api.upload_aws(fn, create_metadata(month),
                              oh_access_token,
                              project_member_id=oh_id)

    gf_member.last_updated = arrow.now().format()
    gf_member.save()
