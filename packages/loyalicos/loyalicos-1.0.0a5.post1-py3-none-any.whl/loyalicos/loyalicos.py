"""
This library allows you to quickly and easily use the Loyalicos Web API v1 via Python.
For more information on this library, see the README on GitHub.

For more information on the Loyalicos API, see:

For the user guide, code examples, and more, visit the main docs page:

This file provides the Loyalicos API Client.
"""

from .simplified_http_client import Response
import os
import requests
from .interface import Interface
from .exceptions import *
import json

class LoyalicosAPIClient(Interface):
    """ Loyaicos basic API client Object
        Extend these to add new objects with API interface.

        Use this object to interact with the Loyalicos API

    """

    def __init__(self, api_key=None, user_token={}, host=None, client_id=None, secret=None):
        self.user_token = user_token
        self.host = host 
        self.api_client = client_id 
        self.api_secret = secret 
        conf = {'LOYALICOS_API_CLIENT': None, 'LOYALICOS_API_SECRET': None, 'LOYALICOS_API_HOST':None, 'LOYALICOS_API_KEY':None }
        env = json.loads(os.environ.get('LOYALICOS_CONF'))
        conf.update(env)
        if self.api_client == None:
            self.api_client = conf.get('LOYALICOS_API_CLIENT')
        if self.api_secret == None:
            self.api_secret = conf.get('LOYALICOS_API_SECRET')
        if self.host == None:
            self.host = conf.get('LOYALICOS_API_HOST')
        self.api_key = api_key 
        if self.api_key == None:
            self.api_key = conf.get('LOYALICOS_API_KEY')
        if self.api_key != None:
            auth = 'Bearer {}'.format(self.api_key)
        else:
            if self.api_client == None or self.api_secret == None:
                raise NoCredentialsFoundError
            else:
                auth_response = requests.get(f'{self.host}/oauth/authapi', auth=requests.auth.HTTPBasicAuth(self.api_client, self.api_secret))
                if auth_response.status_code != 200:
                    raise NoCredentialsFoundError
                auth_result = auth_response.json()
                self.api_key = auth_result.get('token')
                auth = 'Bearer {}'.format(self.api_key)
        super(LoyalicosAPIClient, self).__init__(self.host, auth)
    
    def set_user_token(self, user_token:dict):
        self.user_token.update(user_token)


class Member(LoyalicosAPIClient):
    """
        Extends API Client to handle Members
    """
    def __init__(self, id='', api_key=None, user_token={}, host=None):
        self.id = id
        super(Member, self).__init__(api_key, user_token, host)

    """
        Add a Member
    """
    def create(self, alias=None, data={}):
        self.method = 'POST'
        self.path = ['member']
        self.json = {}
        self.json.update(data)
        self.json.update({"external_id" : alias})
        self.send_request()
        if self.response.status_code != 200:
            if self.response.status_code == 409:
                raise DuplicateKeyForMemberError
            raise HTTPRequestError
        self.access_token = self.response.body

    """
        Get a Member profile
    """
    def read(self, id=None, user_token={}):
        self.user_token.update(user_token)
        if id != None:
            self.id = id
        self.method = 'GET'
        self.path = ['member', self.id]
        user_auth = {self.user_token['token_type'] : self.user_token['access_token']}
        self.update_headers(user_auth)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.profile = self.response.body
        

    """
        Get a Member statement
    """
    def get_awards(self, user_token={}, filter_dict={}):
        filter_string = '|'.join([f"{v}={filter_dict[v]}" for v in filter_dict])
        if filter_dict != {}:
            self.params = f'filters={filter_string}'
        self.user_token.update(user_token)
        self.method = 'GET'
        self.path = ['member', 'awards', self.id]
        user_auth = {self.user_token['token_type'] : self.user_token['access_token']}
        self.update_headers(user_auth)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.awards = self.response.body
        

    """
        Get a Member balance per type and code
    """
    def get_balance(self, type="currency", code="points", user_token={}):
        self.user_token.update(user_token)
        self.method = 'GET'
        self.path = ['member', 'profileValue', self.id, type, code]
        user_auth = {self.user_token['token_type'] : self.user_token['access_token']}
        self.update_headers(user_auth)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.balance = self.response.body

    """
        Post a Signal for the member
    """
    def post_signal(self, signal_data:dict, user_token={}, wait_for_response=False):
        self.user_token.update(user_token)
        signal = Signal(user_token=self.user_token, api_key=self.api_key, host=self.host)
        signal.set_from_dict(signal_data)
        signal.post(member_id=self.id,wait_for_response=wait_for_response)
        return signal

    """
        See if a member has an event type
    """
    def check_event(self,  id=None, user_token={}, search_params={}):
        self.user_token.update(user_token)
        if id != None:
            self.id = id
        self.method = 'POST'
        self.path = ['3PAMI', 'member', 'has_event', self.id]
        self.json = search_params
        user_auth = {self.user_token['token_type'] : self.user_token['access_token']}
        self.update_headers(user_auth)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.event_check = self.response.body.get('result')
        

    """
        Refresh a member token
    """
    def renew_token(self, user_token={}):
        self.user_token.update(user_token)
        self.method = 'POST'
        self.path = ['oauth', 'refreshToken']
        self.json = {'grant_type' : 'refresh_token', 'refresh_token' : user_token['refresh_token'] }
        self.send_request()
        if self.response.status_code != 200:
            if self.response.status_code == 404:
                raise MemberNotFoundError
            raise HTTPRequestError
        self.access_token = self.response.body
        

    """
        Get a new member token
    """
    def new_token(self, id = None):
        if id != None:
            self.id = id
        self.method = 'POST'
        self.path = ['3PAMI', 'accessToken', self.id]
        self.json = {'grant_type' : 'code', 'client_secret' : self.api_secret }
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.access_token = self.response.body

class Event(LoyalicosAPIClient):
    """
        Extends API Client to handle events
    """
    pass

class Signal(LoyalicosAPIClient):
    """
        Extends API Client to handle Signals
    """
    def __init__(self, partner_code='',activity=None, type=None, channel=None,  member_id='', subactivity=None, subtype=None, subchannel=None, currency=None, date_activity=None, items=[], api_key=None, user_token={}, host=None):
        self.partner_code = partner_code
        self.member_id = member_id
        self.activity = activity
        self.type = type
        self.channel = channel
        self.subactivity = subactivity
        self.subtype = subtype
        self.subchannel = subchannel
        self.currency = currency
        self.date_activity = date_activity
        self.items = items
        self.id =""
        self.awards_ids = []
        super(Signal, self).__init__(api_key, user_token, host)

    def set_from_dict(self, data:dict):
        self.make_body()
        for key in self.json:
            if key in data and data[key] != None and data[key] != [] and data[key] != {}:
                self.__setattr__(key,data[key])

    def clear(self):
        self.__init__()
        self.make_body()

    def make_body(self, format='json'):
        if format=='json':
            self.json = {
                'partner_code': self.partner_code,
                'member_id' : self.member_id,
                'date_activity' : self.date_activity,
                'channel': self.channel,
                'subchannel': self.subchannel,
                'type': self.type,
                'subtype': self.subtype,
                'activity': self.activity,
                'subactivity': self.subactivity,
                'currency': self.currency,
                'items': self.items
                }


    def post(self, member_id='', date_activity=None, wait_for_response=False, user_token={}):
        """
            Send Signal
        """
        self.set_user_token(user_token)
        if member_id != '':
           self.member_id = member_id
        if date_activity != None:
           self.date_activity = date_activity
        self.method = 'POST'
        self.path = ['signal']
        self.make_body('json')
        user_auth = {self.user_token['token_type'] : self.user_token['access_token']}
        self.update_headers(user_auth)
        proccess_header = {'Process-Sync' : str(wait_for_response)}
        self.update_headers(proccess_header)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.id = self.response.body['signal_id']
        if wait_for_response:
            self.awards_ids = self.response.body['awards_ids']

    def reward(self, member_id='', user_token={}, date_activity=None):
        """
            Send redemption transaction
        """
        self.post(member_id=member_id, user_token=user_token, date_activity=date_activity, wait_for_response=True)