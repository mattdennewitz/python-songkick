
python-songkick
===============

Wrapping Songkick's API since 2010.

More documentation forthcoming, but check out the example to get started.

Getting an API key
------------------

Visit http://www.songkick.com/api_key_requests/new to request an API key.

Usage
-----

Using this wrapper is fairly straight-forward. Right now, events and
setlists are supported.

Getting a connection
~~~~~~~~~~~~~~~~~~~~

::

    songkick = Songkick(api_key=[YOUR API KEY])

Querying for events
~~~~~~~~~~~~~~~~~~~

``Songkick.events`` provides access to Songkick's event search.

Event querying supports the following parameters:

- ``artist_name``
- ``artist_id``, the Songkick-given artist id
- ``musicbrainz_id``, a MusicBrainz id. If ``musicbrainz_id`` is
  given, no other artist-related query parameters are respected.
- ``venue_id``, the Songkick-given venue id. There is not currently a
  way to programmatically search for venues. 
- ``min_date``, the earliest possible event date. Given as ``date``.
- ``max_date``, the latest possible event date. Given as ``date``.

::
   
    # query for 10 coltrane motion events, no earlier than 1/1/2009
    events = songkick.events.query(artist_name='coltrane motion',
                                   per_page=10,
				   min_date=date(2009, 1, 1))
    
    # iterate over the list of events
    for event in events:
    	print event.display_name	# Coltrane Motion at Arlene's Grocery (June 2, 2010)
	print event.location.city	# New York, NY, US
	print event.venue.display_name	# Arlene's Grocery


Querying for setlists
~~~~~~~~~~~~~~~~~~~~~

``Songkick.setlists`` provides access to Songkick's setlist
catalog.

Right now, Songkick's setlist API only allows querying for setlists by
event id.

::

    # pull the setlist for event 786417, wilco @ the troxy
    setlist = songkick.setlists.get(id=786417)

    # check out whats inside
    print setlist.display_name # Wilco at Troxy (25 Aug 09)

    for song in setlist.setlist_items:
        print song.title # Wilco (The Song)

.. note:: Songkick's API documentation is fairly out of date. I've provided a few response
          examples in the ``data`` dir.
	  	  

Requirements
------------

- python 2.6+
- httplib2
- sphinx (optional, to build docs)
- python-dateutil

All covered in ``requirements.txt``.

TODO
----

- Support event location search
- Pagination feels incomplete, so I'd like to add an optional cursor
  to allow transparent page fetching.


