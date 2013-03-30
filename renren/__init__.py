#!/usr/bin/env python
#coding=utf-8
#
# Copyright 2010 RenRen
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
@author:xiaoba
@home_page : http://blog.xiaoba.me
"""

RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
RENREN_API_SERVER = "http://api.renren.com/restserver.do"


import hashlib
import time
import urllib
import json

parse_json = lambda s: json.loads(s)


class RenRenOauth(object):
    def __init__(self, api_key=None, secret_key=None, scope=None,
                 redirect_uri=None, access_token=None, refresh_token=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_authorize_url(self):
        args = {}
        args["client_id"] = self.api_key
        args["redirect_uri"] = self.redirect_uri
        args["response_type"] = "code"
        args["scope"] = self.scope

        params = urllib.urlencode(args)
        url = RENREN_AUTHORIZATION_URI+"?"+params
        return url

    def get_access_token(self, code):
        args = {}
        args["grant_type"] = "authorization_code"
        args["client_id"] = self.api_key
        args["redirect_uri"] = self.redirect_uri
        args["client_secret"] = self.secret_key
        args["code"] = code

        params = urllib.urlencode(args)
        request = urllib.urlopen(RENREN_ACCESS_TOKEN_URI, params)
        response = request.read()
        request.close()
        response = parse_json(response)
        return response

    def request(self, args):
        """Fetches the given method's response returning from RenRen API.

        Send a POST request to the given method with the given params.
        """
        params = {}
        params["call_id"] = str(int(time.time() * 1000))
        params["format"] = "json"
        params["access_token"] = self.access_token
        params["v"] = '1.0'
        params.update(args)
        sig = self.hash_params(params)
        params["sig"] = sig

        post_data = None if params is None else urllib.urlencode(params)

        #logging.info("request params are: " + str(post_data))

        fetch = urllib.urlopen(RENREN_API_SERVER, post_data)

        try:
            response = fetch.read()
            response = parse_json(response)
        except:
            response = {u'error_msg': u'API Error'}
        finally:
            fetch.close()
        return response

    def hash_params(self, params=None):
        hasher = hashlib.md5("".join(["%s=%s" %
                                      (self.unicode_encode(x),
                                       self.unicode_encode(params[x]))
                                      for x in sorted(params.keys())]))
        hasher.update(self.secret_key)
        return hasher.hexdigest()

    def unicode_encode(self, str):
        """
        Detect if a string is unicode and encode as utf-8 if necessary
        """
        return isinstance(str, unicode) and str.encode('utf-8') or str

    def get_refresh_token(self):
        has_refresh_token = self.refresh_token or None
        assert has_refresh_token, 'refresh_token not found'
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.api_key,
            'client_secret': self.secret_key,
        }
        params = urllib.urlencode(params)
        req = urllib.urlopen(RENREN_ACCESS_TOKEN_URI, params)
        resp = parse_json(req.read())
        self.access_token = resp.get('access_token')
        return resp
