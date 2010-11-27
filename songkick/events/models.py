from songkick.base import SongkickModel
from songkick.fields import *


class SongkickArtistIdentifier(SongkickModel):
    """Universal artist identification.

    :param data_uri: Songkick data outlet URI
    :param musicbrainz_id: A possible MusicBrainz id for this artist
    """
    
    data_uri = Field(mapping='href')
    musicbrainz_id = Field(mapping='mbid')


class SongkickArtist(SongkickModel):
    """A Songkick-described artist.

    :param id: Songkick id
    :param display_name: Artist name, eg, "Neil Young".
    :param songkick_uri: Songkick artist detail uri
    :param identifiers: A list of :ref:`SongkickArtistIdentifier` objects
    :param billing: Event billing status. 'headline' or 'support'.
    :param billing_index: Numerical position on the bill
    """
    
    id = Field()
    display_name = Field(mapping='displayName')
    songkick_uri = Field(mapping='artist__uri')
    identifiers = ListField(ObjectField(SongkickArtistIdentifier),
                            mapping='artist__identifier')
    billing = Field()
    billing_index = Field(mapping='billingIndex')

    def __repr__(self):
        return self.display_name.encode('utf-8')


class SongkickEventDate(SongkickModel):
    """Known times for an event. Used to detail the start
    and, when available, end of a certain event.

    :param date: ``date`` object representing event date. Normally available.
    :param time: ``time`` object representing event time. Sometimes available.
    :param datetime: ``datetime`` object with timezone info. Sometimes available.
    """
    
    date = DateField()
    time = TimeField()
    datetime = DateTimeField()


class SongkickLocation(SongkickModel):
    """Overview of show location, not including venue details.

    :param city: City name. Often sent as City, State, Country, but not guaranteed.
    :param latitude: Latitude
    :param longitude: Longitude
    """
    city = Field()
    latitude = Field(mapping='lat')
    longitude = Field(mapping='lng')


class SongkickMetroArea(SongkickModel):
    id = Field()
    display_name = Field(mapping='displayName')
    country = Field(mapping='country__displayName')


class SongkickVenue(SongkickModel):
    id = Field()
    display_name = Field(mapping='displayName')
    latitude = Field(mapping='lat')
    longitude = Field(mapping='lng')
    metro_area = ObjectField(SongkickMetroArea,
                             mapping='metroArea')
    uri = Field()

    def __repr__(self):
        return self.display_name.encode('utf-8')


class SongkickEventSeries(SongkickModel):
    display_name = Field(mapping='displayName')


class SongkickEvent(SongkickModel):
    id = Field()
    status = Field()
    event_type = Field(mapping='type')
    series = ObjectField(SongkickEventSeries)
    venue = ObjectField(SongkickVenue)
    location = ObjectField(SongkickLocation)
    artists = ListField(ObjectField(SongkickArtist),
                        mapping='performance')
    display_name = Field(mapping='displayName')
    popularity = DecimalField()
    event_start = ObjectField(SongkickEventDate, mapping='start')
    event_end = ObjectField(SongkickEventDate, mapping='end')
    uri = Field()
    
    def __repr__(self):
        return self.display_name.encode('utf-8')

    def is_active(self):
        return bool(self.status == 'ok')

