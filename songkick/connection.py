from urllib import urlencode

import httplib2

from songkick.events.query import EventQuerySet
from songkick.setlists.query import SetlistQuerySet


class Songkick(object):
    "Interface to Songkick services."

    API_ENDPOINT = 'http://api.songkick.com/api/'

    def __init__(self, api_key, version='3.0'):
        
        self.api_key = api_key
        self.version = version
        
        # http client for talking with songkick
        self._http = httplib2.Http('.songkick_cache')

        # set up search providers
        self.events = EventQuerySet(self)
        self.setlists = SetlistQuerySet(self)

    def _make_request(self, url, method='GET', body=None, headers=None):
        "Make an HTTP request"

        headers = headers or {}
        headers['Accept-Charset'] = 'utf-8'

        response, content = self._http.request(url, method, body, headers)

        if int(response.status) != 200:
            raise Exception('Could not load %s: [%s] %s' % \
                                (url, response.status, response.reason))

        return content

    def _build_sk_url(self, api_path, request_args):
        "Assemble the Songkick URL"

        url = Songkick.API_ENDPOINT + self.version + '/' + api_path
        url += "?apikey=" + self.api_key
        url += "&" + urlencode(request_args)
        return url
