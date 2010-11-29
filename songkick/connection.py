import urllib
import urlparse

import httplib2

from songkick.events.query import EventQuerySet
from songkick.exceptions import SongkickRequestError
from songkick.setlists.query import SetlistQuerySet


class Songkick(object):
    "Interface to Songkick services."

    API_ENDPOINT = 'http://api.songkick.com/api/3.0/'

    def __init__(self, api_key):
        
        self.api_key = api_key
        
        # http client for talking with songkick
        self._http = httplib2.Http('.songkick_cache')

        # set up search providers
        self.events = EventQuerySet(self)
        self.setlists = SetlistQuerySet(self)

    def _make_request(self, url, method='GET', body=None, headers=None):
        """Make an HTTP request.

        This could stand to be a little more robust, but Songkick's API
        is very straight-forward: 200 is a success, anything else is wrong.
        """

        headers = headers or {}
        headers['Accept-Charset'] = 'utf-8'

        response, content = self._http.request(url, method, body, headers)

        if int(response.status) != 200:
            raise SongkickRequestError('Could not load %s: [%s] %s' % \
                                       (url, response.status,
                                        response.reason))
        return content

    def _build_sk_url(self, api_path, request_args):
        "Assemble the Songkick URL"

        # insert API key
        request_args['apikey'] = self.api_key

        # construct the complete api resource url, minus args
        url = urlparse.urljoin(Songkick.API_ENDPOINT, api_path)

        # break down the url into its components, inject args
        # as query string and recombine the url
        url_parts = list(urlparse.urlparse(url))
        url_parts[4] = urllib.urlencode(request_args)
        url = urlparse.urlunparse(url_parts)
        
        return url
