from django.db import models
from django.conf import settings
from openhumans.models import OpenHumansMember
from datetime import timedelta
import arrow

import google.oauth2.credentials


def now():
    return arrow.now()


class GoogleFitMember(models.Model):
    """
    Store OAuth2 data for a GoogleFit Member.
    This is a one to one relationship with a OpenHumansMember object.
    """
    user = models.OneToOneField(OpenHumansMember, related_name="googlefit_member", on_delete=models.CASCADE)
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    expiry_date = models.DateTimeField()
    scope = models.CharField(max_length=512)
    last_updated = models.DateTimeField(null=True)
    last_submitted_for_update = models.DateTimeField(null=True)

    @staticmethod
    def get_expiration(expires_in):
        raise Exception('implement me..or delete mee')

    def get_access_token(self):
        """
        Return access token. Refresh first if necessary.
        """
        # Also refresh if nearly expired (less than 60s remaining).
        delta = timedelta(seconds=60)
        if arrow.get(self.expiry_date) - delta < arrow.now():
            self._refresh_tokens()
        return self.access_token

    def _refresh_tokens(self):
        """
        Refresh access token.
        """
        credentials = google.oauth2.credentials.Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            token_uri=settings.GOOGLEFIT_TOKEN_URI,
            client_id=settings.GOOGLEFIT_CLIENT_ID,
            client_secret=settings.GOOGLEFIT_CLIENT_SECRET,
            scopes=settings.GOOGLEFIT_SCOPES,
        )
        if credentials.valid:
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            self.access_token = credentials.token
            if credentials.refresh_token:
                self.refresh_token = credentials.refresh_token
            self.expiry_date = credentials.expiry
            self.save()
            return True
        return False
