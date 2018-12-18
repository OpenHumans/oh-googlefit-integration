"""
Asynchronous tasks that update data in Open Humans.
These tasks:
  1. delete any current files in OH if they match the planned upload filename
  2. adds a data file
"""
import logging
import os
import shutil
import tempfile
import requests
import json
import arrow
from celery import shared_task
from django.conf import settings
from openhumans.models import OpenHumansMember
from datetime import datetime
from googlefit.settings import rr
from main.models import GoogleFitMember
from ohapi import api
from requests_respectful import (RespectfulRequester,
                                 RequestsRespectfulRateLimitedError)
from .googlefit_api import query_data_sources
from .helpers import write_jsonfile_to_tmp_dir

# Set up logging.
logger = logging.getLogger(__name__)


# TODO: we don't need this, we should ideally re-queue a request that hits the exception.
class RateLimitException(Exception):
    """
    An exception that is raised if we reach a request rate cap.
    """

    # TODO: add the source of the rate limit we hit for logging (fitit,
    # internal global googlefit, internal user-specific googlefit)

    pass

def create_metadata():
    return {
        'description':
            'Google Fit data.',
        'tags': ['Google Fit', 'GoogleFit', 'activity', 'steps', 'calories', 'distance'],
        'updated_at': str(datetime.utcnow()),
    }


@shared_task
def fetch_googlefit_data(oh_id):
    '''
    Fetches all of the googlefit data for a given user
    '''
    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
    gf_member = oh_member.googlefit_member
    oh_access_token = oh_member.get_access_token()
    gf_access_token = gf_member.get_access_token()

    data_types_for_user = query_data_sources(gf_access_token)
    out_file = write_jsonfile_to_tmp_dir('foo2.json', {'data_types': data_types_for_user})
    api.upload_aws(out_file, create_metadata(),
                          oh_access_token,
                          project_member_id=oh_id)

    gf_member.last_updated = arrow.now().format()
    gf_member.save()


def get_existing_googlefit(oh_access_token, googlefit_urls):
    print("entered get_existing_googlefit")
    member = api.exchange_oauth2_member(oh_access_token)
    for dfile in member['data']:
        if 'GoogleFit' in dfile['metadata']['tags']:
            print("got inside googlefit if")
            # get file here and read the json into memory
            tf_in = tempfile.NamedTemporaryFile(suffix='.json')
            tf_in.write(requests.get(dfile['download_url']).content)
            tf_in.flush()
            googlefit_data = json.load(open(tf_in.name))
            print("fetched existing data from OH")
            # print(googlefit_data)
            return googlefit_data
    googlefit_data = {}
    for url in googlefit_urls:
        googlefit_data[url['name']] = {}
    return googlefit_data


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
    print("delete response")
    print(deleter)
    print("trying to write to file")
    with open(out_file, 'w') as json_file:
        print("inside open file")
        # json.dump(googlefit_data, json_file)
        json_file.write(json.dumps(googlefit_data))
        # print(json.dump(googlefit_data, json_file))
        print("dumped, trying to flush")
        json_file.flush()
    print("attempting add response")
    addr = api.upload_aws(out_file, metadata,
                   openhumansmember.access_token,
                   project_member_id=openhumansmember.oh_id)
    print("add response")
    print(addr)
    logger.debug('uploaded new file for {}'.format(openhumansmember.oh_id))
