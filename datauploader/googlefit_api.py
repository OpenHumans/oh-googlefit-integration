from datetime import datetime
import requests

from .helpers import get_existing_googlefit_file

# based on the initial release
# https://en.wikipedia.org/wiki/Google_Fit
GOOGLE_FIT_DEFAULT_START_DATE = datetime(2014, 10, 1, 0, 0, 0)


def query_data_sources(access_token):
    headers = {"Content-Type": "application/json;encoding=utf-8",
               "Authorization": "Bearer {}".format(access_token)}
    res = requests.get("https://www.googleapis.com/fitness/v1/users/me/dataSources", headers=headers).json()
    import ipdb;ipdb.set_trace()
    return [res['dataSource'][i]['dataType']['name'] for i in range(len(res['dataSource']))]




def get_googlefit_data(oh_access_token, gf_access_token, current_date):
    # TODO: In the future, extend this to have monthly files

    user_has_data, fn = get_existing_googlefit_file(oh_access_token)

    if user_has_data:
        existing_gf_data = GoogleFitData(fn)
        start_date = existing_gf_data.end_dt
    else:
        existing_gf_data = None
        start_date = GOOGLE_FIT_DEFAULT_START_DATE

    new_gf_data =  GoogleFitData.from_API(gf_access_token, start_date, current_date)

    all_gf_data = new_gf_data.merge(existing_gf_data)

    return all_gf_data




class GoogleFitData(object):

    @property
    def end_dt(self):
        return self._end_dt


    @classmethod
    def from_API(self, access_token, start_dt, end_dt):
        pass


    @classmethod
    def from_file(self, fn):
        # TODO write
        pass

    def merge(self, other_gf_data):
        if other_gf_data is None:
            return self
        pass

    def to_json(self):
        pass

