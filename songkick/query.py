import json
from math import ceil

from songkick.exceptions import SongkickDecodeError


class SongkickQuery(object):

    def __init__(self, connection):
        self._query = {}
        self._result_cache = None
        self._connection = connection

    @classmethod
    def parse_songkick_data(cls, event_data):
        "Parse event data, return ``SongkickResultPage``."
        
        try:
            data = json.loads(event_data)
        except Exception, exc:
            msg = "Couldn't decode response: %s" % exc
            raise SongkickDecodeError(msg)

        # parse results
        page = data['resultsPage']
        results_wrapper = page.get('results')

        if not cls.ResponseEnclosure in results_wrapper:
            raise SongkickDecodeError("%s not found in results page." % \
                                          cls.ResponseEnclosure)

        # pull objects from response
        object_list = results_wrapper.get(cls.ResponseEnclosure)

        for obj in object_list:
            yield cls.ResponseClass._from_json(obj)

    def get_api_path(self):        
        raise NotImplementedError

    def query(self, **query_kwargs):
        """Query Songkick, load results, return data page.

        :param **query_kwargs: All keyword arguments to be converted
                               into a Songkick request.
        :rtype: :class:`SongkickResultPage` containing pagination data
                and results
        """

        # update query args
        self._query = query_kwargs

        # generate songkick url
        url = self._connection.build_songkick_url(self.get_api_path(),
                                                  self._query)

        # request event data
        sk_data = self._connection.make_request(url)

        # parse response
        return self.parse_songkick_data(sk_data)

