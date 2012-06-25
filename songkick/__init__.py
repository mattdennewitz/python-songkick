from connection import SongkickConnection as Songkick


__author__ = 'Matt Dennewitz'
__version__ = '0.0.1'
__version_info__ = tuple(__version__.split('.'))


__all__ = ['Songkick']


def get_version():
    return __version__
