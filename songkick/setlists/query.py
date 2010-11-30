from songkick.query import SongkickQuery
from songkick.setlists.models import SongkickSetlist


class SetlistQuery(SongkickQuery):

    ResponseClass = SongkickSetlist
    ResponseEnclosure = 'setlist'
    
    def get_api_path(self):
        "Generate the API resource path"

        return 'events/%s/setlists.json' % self._query.pop('event_id')

