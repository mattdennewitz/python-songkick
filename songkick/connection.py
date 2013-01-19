import urllib
import urlparse

import httplib2

from songkick.events.query import EventQuery, GigographyQuery
from songkick.exceptions import SongkickRequestError
from songkick.setlists.query import SetlistQuery


class SongkickConnection(object):

    ApiBase = 'http://api.songkick.com/api/3.0/'
    
    def __init__(self, api_key):
        self.api_key = api_key
        self._http = httplib2.Http('.songkick_cache')

    def make_request(self, url, method='GET', body=None, headers=None):
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

    def build_songkick_url(self, api_path, request_args):
        "Assemble the Songkick URL"

        # insert API key
        request_args['apikey'] = self.api_key

        # construct the complete api resource url, minus args
        url = urlparse.urljoin(SongkickConnection.ApiBase, api_path)

        # break down the url into its components, inject args
        # as query string and recombine the url
        url_parts = list(urlparse.urlparse(url))
        url_parts[4] = urllib.urlencode(request_args)
        url = urlparse.urlunparse(url_parts)
        
        return url

    @property
    def events(self):
        return EventQuery(self)

    @property
    def gigography(self):
        return GigographyQuery(self)

    @property
    def setlists(self):
        return SetlistQuery(self)



