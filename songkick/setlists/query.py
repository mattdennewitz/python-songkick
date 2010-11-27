from songkick.query import SongkickQuerySet
from songkick.setlists.models import SongkickSetlist


class SetlistQuerySet(SongkickQuerySet):
    RESPONSE_CLASS = SongkickSetlist
    RESPONSE_ENCLOSURE = 'setlist'
    
    def _get_api_path(self):
        "Generate the API resource path"

        return 'events/%s/setlists.json' % self._query.pop('event_id')

