from songkick.query import SongkickQuery
from songkick.setlists.models import SongkickSetlist


class SetlistQuery(SongkickQuery):

    ResponseClass = SongkickSetlist
    ResponseEnclosure = 'setlist'
    
    def get_api_path(self):
        "Generate the API resource path"

        return 'events/%s/setlists.json' % self._query.pop('event_id')

    def get(self, id):
        """Return a setlist with the given ``id``.

        This method is a bit of a hack, but Songkick's setlist API only
        responds to ids. There is no need to return an iterable.
        """
        
        results = self.query(event_id=id)
        if len(results) > 0:
            return results[0]

