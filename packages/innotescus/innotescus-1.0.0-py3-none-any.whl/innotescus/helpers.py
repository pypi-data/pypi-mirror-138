from datetime import datetime
from functools import wraps, singledispatch
from logging import getLogger
from typing import Dict, Union, Callable
from json.decoder import JSONDecodeError

import requests
from google.protobuf.timestamp_pb2 import Timestamp

from ._grpc.ApiCommon_pb2 import TimestampRange
from .datatypes import DateRange
from .exceptions import YankedVersionError

log = getLogger('innotescus')


def ttl_cache_from_dict_result(f: Callable) -> Callable:
    """ Wrapper for caching the result of a function/method call.
    Cache value TTL expected from result value in key 'expires_at', which
    must be an unix timestamp.
    """
    expiry_time: Union[datetime, None] = None
    cached_response: Union[Dict, None] = None

    @wraps(f)
    def inner(*args, **kwargs):
        nonlocal expiry_time, cached_response

        if cached_response is not None:
            if expiry_time <= datetime.utcnow():  # assume expiry_time is in utc
                log.debug('TTL expired, evicting cached value')
                cached_response, expiry_time = None, None
            else:
                log.debug('Returning cached value')
                return cached_response

        rv = f(*args, **kwargs)

        if type(rv) is dict and 'expires_at' in rv:
            expiry_time = datetime.fromtimestamp(rv['expires_at'])  # DO NOT convert to UTC -- should already be UTC
            cached_response = rv
        else:
            log.debug('Failed to cache result.')

        return rv

    return inner


def _get_current_version():
    from . import __version__  # local import to avoid circular ref
    return __version__


def check_for_yanked_release():
    """ Ensures the user's version of Innotescus hasn't been removed
    from the pypi repository.  If it has, raise an error.
    """
    try:
        release_info =  requests.get('https://pypi.org/pypi/innotescus/json').json()['releases'][_get_current_version()]
        yanked = [row for row in release_info if row['yanked']]
        if yanked:
            raise YankedVersionError(yanked[0]['yanked_reason'])
    except KeyError:
        log.warning(f'Could not find "innotescus" version {_get_current_version()} on pypi')
    except JSONDecodeError:
        log.warning('Could not check for yanked version from pypi')


def check_for_updates():
    """ Checks PYPI for newer major/minor versions of innotescus and emits a warning if
    found.
    """
    try:
        latest_version = requests.get('https://pypi.org/pypi/innotescus/json').json()['info']['version']
        current = _get_current_version().split('.')
        latest = latest_version.split('.')
        MAJOR, MINOR, PATCH = 0, 1, 2
        if int(latest[MAJOR]) > int(current[MAJOR]) or int(latest[MINOR]) > int(current[MINOR]):
            log.warning(f'There is a new version of innotescus ({latest_version}).  Please update immediately')
    except JSONDecodeError:
        log.warning('Could not check latest version from pypi')


def deprecated(message: str) -> Callable:
    """ Simple wrapper that outputs a warning message when the wrapped object is called.
    """
    def wrapper(f: Callable) -> Callable:
        @wraps(f)
        def inner(*args, **kwargs):
            log.warning('[DEPRECATED] %s', message)
            return f(*args, **kwargs)
        return inner
    return wrapper


@singledispatch
def to_grpc(arg):
    raise RuntimeError('Invalid argument type for conversion')


@to_grpc.register
def _(arg: DateRange):
    start, end, = Timestamp(), Timestamp(),
    start.FromDatetime(arg.start)
    end.FromDatetime(arg.end)
    return TimestampRange(start=start, end=end)
