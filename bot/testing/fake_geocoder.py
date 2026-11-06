from collections.abc import Mapping
from contextlib import AbstractContextManager
from typing import Any
from unittest.mock import patch

from geopy.exc import GeocoderServiceError
from geopy.location import Location

from bot.utils import location


class FakeGeocoder:
    """Находит только заданные адреса и отвечает в формате Nominatim."""

    def __init__(self, places: Mapping[str, tuple[str, str]]) -> None:
        self._places = places

    def geocode(self, query: str, **options: Any) -> Location | None:
        if query not in self._places:
            return None
        city, country = self._places[query]
        return Location(query, (0.0, 0.0), {"address": {"city": city, "country": country}})


class _FailingGeocoder:
    def __init__(self, error: GeocoderServiceError) -> None:
        self._error = error

    def geocode(self, query: str, **options: Any) -> Location | None:
        raise self._error


def geocoding_of(places: Mapping[str, tuple[str, str]]) -> AbstractContextManager[Any]:
    return patch.object(location, "geolocator", FakeGeocoder(places))


def geocoding_failure(error: GeocoderServiceError) -> AbstractContextManager[Any]:
    return patch.object(location, "geolocator", _FailingGeocoder(error))
