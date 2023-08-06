import os
import pathlib
import json
from time import sleep

import requests


WAIT_SECONDS = 3
API_VERSION = 'v1'

def _check_for_error(r):
    if not r.ok:
        print(json.dumps(json.loads(r.text), indent=4))
    r.raise_for_status()


class Base:
    def __init__(self):
        self.token = ''
        self.host = ''

    def init(self, token, host='https://api.dynamofl.com'):
        self.host = host
        self.token = token

    def _get_route(self):
        return f'{self.host}/{API_VERSION}'

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.token}'}

    def make_request(self, method, url, params=None, files=None, list=False):
        if method == 'POST':
            r = requests.post(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                json=params,
                files=files
            )
        elif method == 'GET':
            r = requests.get(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                params=params
            )
        elif method == 'DELETE':
            r = requests.delete(
                f'{self._get_route()}{url}',
                headers=self._get_headers()
            )

        _check_for_error(r)

        if r.content:
            if list:
                return r.json()['data']
            else:
                return r.json()



class _Project(Base):
    def __init__(self, host, token, key):
        super().__init__()
        self.init(token, host)
        self.key = key
    
    def get_info(self):
        return self.make_request('GET', f'/projects/{self.key}')

    def update_rounds(self, rounds):
        return self.make_request('POST', f'/projects/{self.key}', params={'rounds': rounds})

    def update_schedule(self, schedule):
        return self.make_request('POST', f'/projects/{self.key}', params={'schedule': schedule})

    def update_paused(self, paused):
        return self.make_request('POST', f'/projects/{self.key}', params={'paused': paused})

    def update_auto_increment(self, auto_increment):
        return self.make_request('POST', f'/projects/{self.key}', params={'autoIncrement': auto_increment})

    def update_optimizer_params(self, optimizer_params):
        return self.make_request('POST', f'/projects/{self.key}', params={'optimizerParams': optimizer_params})

    def delete_project(self):
        return self.make_request('DELETE', f'/projects/{self.key}')

    def add_contributor(self, email, role='member'):
        return self.make_request('POST', f'/projects/{self.key}/contributors', params={'email': email, 'role': role})

    def delete_contributor(self, email):
        return self.make_request('DELETE', f'/projects/{self.key}/contributors', params={'email': email})

    def get_next_schedule(self):
        return self.make_request('GET', f'/projects/{self.key}/schedule')

    def increment_round(self):
        return self.make_request('POST', f'/projects/{self.key}/increment')

    def create_datalink(self, datalink_key, description=None):
        params = {'key': datalink_key}
        if description:
            params['description'] = description
        return self.make_request('POST', f'/projects/{self.key}/datalinks', params=params)

    def get_datalinks(self):
        return self.make_request('GET', f'/projects/{self.key}/datalinks', list=True)

    def get_datalink(self, datalink_key):
        return self.make_request('GET', f'/projects/{self.key}/datalinks/{datalink_key}')

    def delete_datalink(self, datalink_key):
        return self.make_request('DELETE', f'/projects/{self.key}/datalinks/{datalink_key}')

    def get_rounds(self):
        return self.make_request('GET', f'/projects/{self.key}/rounds', list=True)

    def get_round(self, round):
        return self.make_request('GET', f'/projects/{self.key}/rounds/{round}')

    def get_stats(self, round=None, datalink_key=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datalink_key is not None:
            params['datalink'] = datalink_key
        return self.make_request('GET', f'/projects/{self.key}/stats', params, list=True)

    def get_stats_avg(self):
        return self.make_request('GET', f'/projects/{self.key}/stats/avg')

    def get_submissions(self, datalink_key=None, round=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datalink_key is not None:
            params['datalink'] = datalink_key
        return self.make_request('GET', f'/projects/{self.key}/submissions', params, list=True)

    def wait_for_round_to_end(self, round, throw_on_federation_error=False):
        federation_error = None
        while True:
            j = self.make_request('GET', f'/projects/{self.key}/rounds/{round}')

            if j and j['federationError']:
                if throw_on_federation_error:
                    raise Exception(j)
                if federation_error != j['federationError']:
                    federation_error = j['federationError']
                    print('Federation error occured:\n  ' + federation_error)
            if j and j['endTime']:
                return
            sleep(WAIT_SECONDS)

    def upload_optimizer(self, path):
        with open(path, 'rb') as f:
            self.make_request('POST', f'/projects/{self.key}/optimizers', files={'optimizer': f})




    def report_stats(self, scores, num_samples, round, datalink_key):
        return self.make_request('POST', f'/projects/{self.key}/stats', params={
            'round': round,
            'scores': scores,
            'numPoints': num_samples,
            'datalink': datalink_key
        })

    def push_model(self, path, datalink_key, params=None):
        if params is not None:
            self.make_request('POST', f'/projects/{self.key}/models/{datalink_key}/params', params=params)

        if datalink_key is None:
            url = f'/projects/{self.key}/models'
        else:
            url = f'/projects/{self.key}/models/{datalink_key}'
        with open(path, 'rb') as f:
            self.make_request('POST', url, files={'modelfile': f})

    def pull_model(self, filepath, datalink_key=None, round=None, throw_error=False):
        params = {}
        if round is not None:
            params['round'] = round

        if round is not None and datalink_key is None:
            self.wait_for_round_to_end(round, throw_on_federation_error=throw_error)


        if datalink_key is None:
            url = f'{self._get_route()}/projects/{self.key}/models'
        else:
            url = f'{self._get_route()}/projects/{self.key}/models/{datalink_key}'
        r = requests.get(url, headers=self._get_headers(), params=params)
        _check_for_error(r)

        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)


class _Client(Base):
    def __init__(self):
        super().__init__()

    def _check_init(self):
        if not self.host or not self.token:
            raise ValueError('Must call init() first, passing in API key.')

    def get_user(self):
        return self.make_request('GET', f'/user')

    def create_project(self, base_model_path, params):
        self._check_init()

        j = self.make_request('POST', '/projects', params=params)

        project = _Project(self.host, self.token, j['key'])
        project.push_model(base_model_path, None)

        return project

    def get_project(self, project_key):
        self._check_init()
        j = self.make_request('GET', f'/projects/{project_key}')
        return _Project(self.host, self.token, j['key'])

    def get_projects(self):
        self._check_init()
        return self.make_request('GET', f'/projects', list=True)


client = _Client()

init = client.init
get_user = client.get_user
create_project = client.create_project
get_project = client.get_project
get_projects = client.get_projects