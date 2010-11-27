from songkick.base import SongkickModel
from songkick.events.models import SongkickArtistIdentifier
from songkick import fields


class SongkickSetlistItem(SongkickModel):
    song_title = fields.Field(mapping='name')
    encore = fields.BooleanField()


class SongkickSetlistArtist(SongkickModel):
    """Artist representations are not consistent between resources,
    so we have to redefine a simpler artist model for setlists.
    """
    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    identifiers = fields.ListField(fields.ObjectField(SongkickArtistIdentifier))
    songkick_uri = fields.Field(mapping='uri')


class SongkickSetlist(SongkickModel):
    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    artist = fields.ObjectField(SongkickSetlistArtist)
    setlist = fields.ListField(fields.ObjectField(SongkickSetlistItem),
                               mapping='setlistItem')    


