python-songkick
===============

Wrapping Songkick's API since 2010.

More documentation forthcoming, but check out the example to get started.

Usage
-----

Using this wrapper is fairly straight-forward: ::

    # get a connection to songkick
    >>> songkick = Songkick(api_key=[YOUR API KEY])
    
    # query for 'page 1' of coltrane motion events, 10 events per page
    >>> events_page = songkick.events.query(artist_name='coltrane motion',
                                            per_page=10)
    
    # querying returns a page of events, and pagination data
    >>> events_page.object_count
    47

    >>> events_page.page_count
    5

    >>> events_page.page_number
    1

    >>> events_page.next_page_number()
    2

    # iterate over the list of events
    for event in events_page:
    	print event.display_name	# Coltrane Motion at Arlene's Grocery (June 2, 2010)
	print event.location.city	# New York, NY, US
	print event.venue.display_name	# Arlene's Grocery

Requirements
------------

- python 2.6+
- httplib2
- sphinx (optional, to build docs)
- python-dateutil

All covered in ``requirements.txt``.

Plans
-----

- Documentation, y'know?
- Sprinkle in unit tests
- Implement user methods
