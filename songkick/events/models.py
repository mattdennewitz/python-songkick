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
    """A metro area, used to describe where a :ref:`SongkickVenue`
    is located.

    :param id: Songkick id
    :param display_name: Metro area name
    :param country: Country name
    """

    id = Field()
    display_name = Field(mapping='displayName')
    country = Field(mapping='country__displayName')


class SongkickVenue(SongkickModel):
    """Event venue.

    :param id: Songkick id
    :param display_name: Venue name
    :param latitude: Venue latitude
    :param longitude: Venue longitude
    :param metro_area: The :ref:`SongkickMetroArea` describing where this venue's location
    :param uri: Songkick venue data uri
    """
    
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
    """Serial show wrapper name. Useful for describing long-running
    events, like festivals.

    :param display_name: Series name
    """

    display_name = Field(mapping='displayName')


class SongkickEvent(SongkickModel):
    """An event tracked by Songkick.

    :param id: Songkick id
    :param status: Event status. Normally 'ok', sometimes 'cancelled'.
    :param event_type: Event type. 'concert' or 'festival'.
    :param venue: :ref:`SongkickVenue` object
    :param location: :ref:`SongkickLocation` object
    :param artists: Collection of artists (via :ref:`SongkickArtist`)
                    performing at this event.
    :param display_name: Event title
    :param popularity: Popularity measurement for this event
    :param event_start: Start date and (sometimes) time for this event
    :param event_end: End date and (sometimes) time for this event.
                      Not often populated, and normally only seen
                      with festivals.
    :param uri: Songkick data uri
    """
    
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

