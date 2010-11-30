from songkick.base import SongkickModel
from songkick.events.models import SongkickArtistIdentifier
from songkick import fields


class SongkickSetlistItem(SongkickModel):
    """A setlist entry.

    :param song_title: Title of the song or piece
    :param encore: Boolean value stating if this was part of an encore
    """

    title = fields.Field(mapping='name')
    encore = fields.BooleanField()


class SongkickSetlistArtist(SongkickModel):
    """Setlist artist summary.

    :param id: Songkick artist id
    :param display_name: Artist's name
    :param songkick_uri: Songkick artist detail uri
    :param identifiers: A list of :ref:`SongkickArtistIdentifier` objects

    .. note:: Artist representations are not consistent between resources,
              so we have to redefine a simpler artist model for setlists.
    """

    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    songkick_uri = fields.Field(mapping='uri')
    identifiers = fields.ListField(fields.ObjectField(SongkickArtistIdentifier))


class SongkickSetlist(SongkickModel):
    """An event's setlist.

    :param id: Songkick setlist id
    :param display_name: Setlist name
    :param artist: :class:`SongkickSetlistArtist` object representing the
                   performing artist
    :param setlist: Songs or pieces performed in this set, as a list of
                    :class:`SongkickSetlistItem` objects.
    """

    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    artist = fields.ObjectField(SongkickSetlistArtist)
    setlist_items = fields.ListField(fields.ObjectField(SongkickSetlistItem),
                                     mapping='setlistItem')    

    def __repr__(self):
        return self.display_name.encode('utf-8')

