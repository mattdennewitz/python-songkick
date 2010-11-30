from songkick.events.models import SongkickEvent
from songkick.query import SongkickQuerySet


class EventQuerySet(SongkickQuerySet):
    "Events-specific query backend"
    
    ResponseClass = SongkickEvent
    ResponseEnclosure = 'event'
    
    def _get_api_path(self):
        "Generate the API resource path"

        if 'musicbrainz_id' in self._query:
            return 'artists/mbid:%s/events.json' % \
                   self._query.pop('musicbrainz_id')
        return 'events.json'

