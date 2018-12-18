import requests

def query_data_sources(access_token):
    headers = {"Content-Type": "application/json;encoding=utf-8",
               "Authorization": "Bearer {}".format(access_token)}
    res = requests.get("https://www.googleapis.com/fitness/v1/users/me/dataSources", headers=headers).json()
    return [res['dataSource'][i]['dataType']['name'] for i in range(len(res['dataSource']))]