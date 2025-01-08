"""
REMSutils
"""

import requests
import json
import urllib.parse

REQUEST = {'get': requests.get,
           'post': requests.post,
           'put': requests.put
           }


class REMSinstance(object):
    """
    Class to manage REMS instance
    """
    def __init__(self, rems_url, api_key, user_id):
        """
        Constructor for class REMSinstance
        """
        self.rems_url = rems_url
        self.api_key = api_key
        self.user_id = user_id

    def request(self, api_endpoint, headers=None, data=None, params=None, request_type='get'):
        full_url = f'{self.rems_url}{api_endpoint}'
        full_headers = {
            'accept': 'application/json',
            'x-rems-api-key': self.api_key,
            'x-rems-user-id': self.user_id
            }
        if headers:
            full_headers.update(headers)

        response = REQUEST[request_type](
            url=full_url,
            params=params,
            headers=full_headers,
            data=data
            )

        return response



class REMSuser:
    def get_users(self):
        response = self.rems_instance.request('/api/applications/members', params={'disabled': 'false', 'archived': 'false'})
        assert response.status_code == 200, f'status_code = {response.status_code}, text = {response.text}'
        return response.json()

    def get_user(self, user_dict):
        matching_users = [user for user in self.get_users() if all([user.get(key) == user_dict[key] for key in user_dict.keys()])]
        assert len(matching_users) <= 1, f'Multiple matches found for {user_dict}: {matching_users}'

        if matching_users:
            return matching_users[0]
        else:
            return None

    def create_user(self, user_dict):
        assert set(user_dict.keys()).issuperset({'userid', 'name', 'email'}), \
            "Must supply at least user_id, user_name, and user_email to create a new user"

        response = self.rems_instance.request('/api/users/create',
                                              data=json.dumps(user_dict),
                                              headers={'Content-Type': 'application/json'},
                                              request_type='post'
                                              )
        assert response.status_code == 200, f'status_code = {response.status_code}, text = {response.text}'
        return user_dict



    def __init__(self, rems_instance, user_dict):
        self.rems_instance = rems_instance

        assert set(user_dict.keys()).intersection({'userid', 'name', 'email'}), \
            "Must supply at least one of user_id, user_name, or user_email"

        self.data = self.get_user(user_dict) or self.create_user(user_dict)


class REMSorganization:
    def get_orgs(self):
        response = self.rems_instance.request('/api/organizations', params={'disabled': 'false', 'archived': 'false'})
        assert response.status_code == 200, f'status_code = {response.status_code}, text = {response.text}'
        return response.json()

    def get_org(self, org_dict):
        matching_orgs = [org for org in self.get_orgs() if all([org.get(key) == org_dict[key] for key in org_dict.keys()])]
        assert len(matching_orgs) <= 1, f'Multiple matches found for {org_dict}: {matching_orgs}'

        if matching_orgs:
            return matching_orgs[0]
        else:
            return None

    def get_org_by_id(self, org_id):
        response = self.rems_instance.request(f'/api/organizations/{urllib.parse.quote_plus(org_id)}')
        assert response.status_code == 200, f'status_code = {response.status_code}, text = {response.text}'
        return response.json()

    def create_org(self, org_dict):
        assert set(org_dict.keys()).issuperset({'organization/id', 'organization/short-name', 'organization/name', 'organization/owners', 'organization/review-emails'}), \
            "Must supply at least 'organization/id', 'organization/short-name', 'organization/name', 'organization/owners', 'organization/review-emails' to create a new organization"

        response = self.rems_instance.request('/api/organizations/create',
                                              data=json.dumps(org_dict),
                                              headers={'Content-Type': 'application/json'},
                                              request_type='post'
                                              )
        assert response.status_code == 200, f'status_code = {response.status_code}, text = {response.text}'
        return org_dict



    def __init__(self, rems_instance, org_dict):
        self.rems_instance = rems_instance

        assert set(org_dict.keys()).intersection({'organization/id', 'organization/short-name', 'organization/name'}), \
            "Must supply at least one of 'organization/id', 'organization/short-name', or 'organization/name'"

        self.data = self.get_org(org_dict) or self.create_org(org_dict)

