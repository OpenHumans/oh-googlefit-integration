from datetime import datetime, timedelta
import logging
import arrow

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from datauploader.tasks import fetch_googlefit_data
from datauploader.googlefit_api import (get_latest_googlefit_file_url,
                                        get_latest_googlefit_file_updated_dt)
from ohapi import api
from openhumans.models import OpenHumansMember
from .models import GoogleFitMember
import google_auth_oauthlib.flow


# Set up logging.
logger = logging.getLogger(__name__)


def index(request):
    """
    Starting page for app.
    """
    if request.user.is_authenticated:
        if hasattr(request.user.openhumansmember, 'googlefit_member'):
            return redirect('dashboard')
        else:
            return redirect('setup')
    else:
        context = {'oh_auth_url': OpenHumansMember.get_auth_url()}
        return render(request, 'main/index.html', context=context)


def about(request):
    """
    Share further details about the project.
    """
    return render(request, 'main/about.html')


def setup(request):
    """
    Set up Google Fit connection.
    """
    if not request.user.is_authenticated:
        return redirect('index')
    context = {}
    if not hasattr(request.user.openhumansmember, 'googlefit_member'):
        context['gf_auth_url'] = reverse('authorize_googlefit')
    return render(request, 'main/setup.html', context=context)


def logout_user(request):
    """
    Logout user.
    """
    if request.method == 'POST':
        logout(request)
    redirect_url = settings.LOGOUT_REDIRECT_URL
    return redirect(redirect_url)


def dashboard(request):

    def can_update_data(googlefit_member):
        if not googlefit_member.last_submitted_for_update or googlefit_member.last_submitted_for_update < (
            arrow.now() - timedelta(hours=1)):
            return True
        return False

    if not request.user.is_authenticated:
        return redirect('index')

    if not hasattr(request.user.openhumansmember, 'googlefit_member'):
        return redirect('setup')

    googlefit_member = request.user.openhumansmember.googlefit_member

    ### removed as part of template standardization - MPB 201902
    # download_file = get_latest_googlefit_file_url(request.user.openhumansmember.get_access_token())
    # last_updated = get_latest_googlefit_file_updated_dt(request.user.openhumansmember.get_access_token())
    # if download_file == 'error':
    #     logout(request)
    #     return redirect("/")

    try:
        data_files = request.user.openhumansmember.list_files()
        data_files.sort(key=lambda x: x['basename'], reverse=True)
    except Exception:
        data_files = None

    last_updated = get_latest_googlefit_file_updated_dt(
        request.user.openhumansmember.get_access_token())
    allow_update = can_update_data(googlefit_member) or last_updated is None
    context = {
        'openhumansmember': request.user.openhumansmember,
        'googlefit_member': googlefit_member,
        'data_files': data_files,
        'timedelta_since_update': arrow.get(last_updated).humanize(
            granularity='hour'),
        'allow_update': allow_update,
    }
    return render(request, 'main/dashboard.html',
                    context=context)


def authorize_googlefit(request):
    # Create google oauth flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        settings.GOOGLEFIT_CLIENT_CONFIG, scopes=settings.GOOGLEFIT_SCOPES)

    flow.redirect_uri = request.build_absolute_uri(reverse('complete_googlefit'))

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    request.session['googlefit_oauth2_state'] = state

    return redirect(authorization_url)

def complete_googlefit(request):

    if 'googlefit_oauth2_state' not in request.session:
        messages.warning('Authorization with google did not succeed. Please try again')
        return redirect('/dashboard')

    state = request.session['googlefit_oauth2_state']
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        settings.GOOGLEFIT_CLIENT_CONFIG, scopes=settings.GOOGLEFIT_SCOPES,
        state=state)
    flow.redirect_uri = request.build_absolute_uri(reverse('complete_googlefit'))


    authorization_response = settings.OPENHUMANS_APP_BASE_URL + request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    if hasattr(request.user.openhumansmember, 'googlefit_member'):
        googlefit_member = request.user.openhumansmember.googlefit_member
    else:
        googlefit_member = GoogleFitMember()

    googlefit_member.access_token = credentials.token
    if credentials.refresh_token:
        # Google returns a null refresh token after the 1st time
        googlefit_member.refresh_token = credentials.refresh_token
    googlefit_member.expiry_date = credentials.expiry
    googlefit_member.scope = credentials.scopes
    googlefit_member.user_id = request.user.openhumansmember.oh_id
    googlefit_member.save()

    fetch_googlefit_data.delay(request.user.openhumansmember.oh_id, send_email=True)

    if googlefit_member and googlefit_member.refresh_token:
        messages.info(request, "Your GoogleFit account has been connected, and your data has been queued to be fetched from GoogleFit. You will receive an e-mail when the process has completed.")
        return redirect('dashboard')

    logger.debug('Invalid code exchange. User returned to starting page.')
    messages.warning(request, ("Something went wrong, please try connecting your "
                            "GoogleFit account again. If you have an existing connection, please go to https://myaccount.google.com/permissions to remove it and try again."))
    return redirect('dashboard')


def remove_googlefit(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            openhumansmember = request.user.openhumansmember
            api.delete_file(openhumansmember.access_token,
                            openhumansmember.oh_id,
                            file_basename="googlefit-data.json")
            messages.info(request, "Your GoogleFit account has been removed")
            googlefit_account = request.user.openhumansmember.googlefit_member
            googlefit_account.delete()
        except:
            googlefit_account = request.user.openhumansmember.googlefit_member
            googlefit_account.delete()
            messages.info(request, ("Something went wrong, please"
                          "re-authorize us on Open Humans"))
            logout(request)
            return redirect('/')
    return redirect('/dashboard')


def update_data(request):
    if request.method == "POST" and request.user.is_authenticated:
        openhumansmember = request.user.openhumansmember
        googlefit_member = openhumansmember.googlefit_member
        last_updated = get_latest_googlefit_file_updated_dt(openhumansmember.get_access_token())
        send_email = last_updated is None
        fetch_googlefit_data.delay(openhumansmember.oh_id, send_email=send_email)
        googlefit_member.last_submitted_for_update = arrow.now().format()
        googlefit_member.save()
        messages.info(request,
                      ("An update of your GoogleFit data has been started! "
                       "It can take some minutes before the first data is "
                       "available. Reload this page in a while to find your "
                       "data."))
        return redirect('/dashboard')
