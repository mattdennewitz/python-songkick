from songkick.base import SongkickModel
from songkick import fields


class SongkickArtistIdentifier(SongkickModel):
    """Universal artist identification.

    :param data_uri: Songkick data outlet URI
    :param musicbrainz_id: A possible MusicBrainz id for this artist

    .. note:: Songkick stores multiple identifiers for artists
              with non-unique names. For example, Songkick stores
              seven possible MusicBrainz ids for the swedish pop duo
              "jj", because there are at least seven acts releasing
              under that name. It's up to the client to store
              and match the correct MusicBrainz id.
    """
    
    data_uri = fields.Field(mapping='href')
    musicbrainz_id = fields.Field(mapping='mbid')


class SongkickArtist(SongkickModel):
    """A Songkick-described artist.

    :param id: Songkick id
    :param display_name: Artist name, eg, "Neil Young".
    :param songkick_uri: Songkick artist detail uri
    :param identifiers: A list of :class:`SongkickArtistIdentifier` objects
    :param billing: Event billing status. 'headline' or 'support'.
    :param billing_index: Numerical position on the bill
    """
    
    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    songkick_uri = fields.Field(mapping='artist__uri')
    identifiers = fields.ListField(fields.ObjectField(SongkickArtistIdentifier),
                                   mapping='artist__identifier')
    billing = fields.Field()
    billing_index = fields.Field(mapping='billingIndex')

    def __repr__(self):
        return self.display_name.encode('utf-8')


class SongkickEventDate(SongkickModel):
    """Known times for an event. Used to detail the start
    and, when available, end of a certain event.

    :param date: ``date`` object representing event date. Normally available.
    :param time: ``time`` object representing event time. Sometimes available.
    :param datetime: ``datetime`` object with timezone info. Sometimes available.
    """
    
    date = fields.DateField()
    time = fields.TimeField()
    datetime = fields.DateTimeField()


class SongkickLocation(SongkickModel):
    """Overview of show location, not including venue details.

    :param city: City name. Often sent as City, State, Country,
                 but no particular format is enforced.
    :param latitude: Latitude
    :param longitude: Longitude
    """

    city = fields.Field()
    latitude = fields.Field(mapping='lat')
    longitude = fields.Field(mapping='lng')


class SongkickMetroArea(SongkickModel):
    """A metro area, used to describe where a :class:`SongkickVenue`
    is located.

    :param id: Songkick id
    :param display_name: Metro area name
    :param country: Country name
    """

    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    country = fields.Field(mapping='country__displayName')


class SongkickVenue(SongkickModel):
    """Event venue.

    :param id: Songkick id
    :param display_name: Venue name
    :param latitude: Venue latitude
    :param longitude: Venue longitude
    :param metro_area: The :class:`SongkickMetroArea` describing this
                       venue's location
    :param uri: Songkick venue data uri
    """
    
    id = fields.Field()
    display_name = fields.Field(mapping='displayName')
    latitude = fields.Field(mapping='lat')
    longitude = fields.Field(mapping='lng')
    metro_area = fields.ObjectField(SongkickMetroArea,
                                    mapping='metroArea')
    uri = fields.Field()

    def __repr__(self):
        return self.display_name.encode('utf-8')


class SongkickEventSeries(SongkickModel):
    """Serial show wrapper name. Useful for describing long-running
    events, like festivals.

    :param display_name: Series name
    """

    display_name = fields.Field(mapping='displayName')


class SongkickEvent(SongkickModel):
    """An event tracked by Songkick.

    :param id: Songkick id
    :param status: Event status. Normally 'ok', sometimes 'cancelled'.
    :param event_type: Event type. 'concert' or 'festival'.
    :param venue: :class:`SongkickVenue` object
    :param location: :class:`SongkickLocation` object
    :param artists: Collection of artists (via :class:`SongkickArtist`)
                    performing at this event.
    :param display_name: Event title
    :param popularity: Popularity measurement for this event
    :param event_start: Start date and (sometimes) time for this event
    :param event_end: End date and (sometimes) time for this event.
                      Not often populated, and normally only seen
                      with festivals.
    :param uri: Songkick data uri
    """
    
    id = fields.Field()
    status = fields.Field()
    event_type = fields.Field(mapping='type')
    series = fields.ObjectField(SongkickEventSeries)
    venue = fields.ObjectField(SongkickVenue)
    location = fields.ObjectField(SongkickLocation)
    artists = fields.ListField(fields.ObjectField(SongkickArtist),
                               mapping='performance')
    display_name = fields.Field(mapping='displayName')
    popularity = fields.DecimalField()
    event_start = fields.ObjectField(SongkickEventDate, mapping='start')
    event_end = fields.ObjectField(SongkickEventDate, mapping='end')
    uri = fields.Field()
    
    def __repr__(self):
        return self.display_name.encode('utf-8')

    def is_active(self):
        return bool(self.status == 'ok')

