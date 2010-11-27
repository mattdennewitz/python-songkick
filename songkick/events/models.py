from songkick.base import SongkickModel
from songkick.fields import *


class SongkickArtistIdentifier(SongkickModel):
    data_uri = Field(mapping='href')
    musicbrainz_id = Field(mapping='mbid')


class SongkickArtist(SongkickModel):
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
    date = DateField()
    time = TimeField()
    datetime = DateTimeField()


class SongkickLocation(SongkickModel):
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

