"""
Asynchronous tasks that update data in Open Humans.
These tasks:
  1. delete any current files in OH if they match the planned upload filename
  2. adds a data file
"""
import logging
import os

import tempfile
import json
import arrow
from celery import shared_task

from openhumans.models import OpenHumansMember
from datetime import datetime
from ohapi import api

from .googlefit_api import query_data_sources
from .helpers import write_jsonfile_to_tmp_dir

# Set up logging.
logger = logging.getLogger(__name__)


def create_metadata():
    return {
        'description':
            'Google Fit data.',
        'tags': ['Google Fit', 'GoogleFit', 'activity', 'steps', 'calories', 'distance'],
        'updated_at': str(datetime.utcnow()),
        'month': '',
    }


@shared_task
def fetch_googlefit_data(oh_id, current_dt):
    '''
    Fetches all of the googlefit data for a given user
    '''
    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
    gf_member = oh_member.googlefit_member
    oh_access_token = oh_member.get_access_token()
    gf_access_token = gf_member.get_access_token()

    data_types_for_user = query_data_sources(gf_access_token)
    out_file = write_jsonfile_to_tmp_dir('data.json', {'data_types': data_types_for_user})
    api.upload_aws(out_file, create_metadata(),
                          oh_access_token,
                          project_member_id=oh_id)

    gf_member.last_updated = arrow.now().format()
    gf_member.save()


def replace_googlefit(openhumansmember, googlefit_data):
    print("replace function started")
    # delete old file and upload new to open humans
    tmp_directory = tempfile.mkdtemp()
    metadata = {
        'description':
        'GoogleFit data.',
        'tags': ['GoogleFit', 'activity', 'steps'],
        'updated_at': str(datetime.utcnow()),
        }
    out_file = os.path.join(tmp_directory, 'googlefit-data.json')
    logger.debug('deleted old file for {}'.format(openhumansmember.oh_id))
    deleter = api.delete_file(openhumansmember.access_token,
                    openhumansmember.oh_id,
                    file_basename="googlefit-data.json")

