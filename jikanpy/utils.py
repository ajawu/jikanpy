"""Jikan/AioJikan Utilities
====================================
utils.py contains utility methods used in Jikan and AioJikan.
"""

from typing import Optional, Dict, Mapping, Union, Any

import aiohttp
import requests

from jikanpy.exceptions import APIException

BASE_URL = "https://api.jikan.moe/v3"


def check_response(
    response_dict: Dict[str, Any],
    response_status_code: int,
    **kwargs: Union[int, Optional[str]],
) -> None:
    """
        Check if the response is an error

        Keyword Arguments:
        response_dict -- parsed response from the API call
                         is empty ({}) when there was a json.decoder.JSONDecodeError
        response_status -- the corresponding http code for the response
        kwargs -- keyword arguments
        """
    if response_status_code >= 400:
        error_msg = response_dict.get("error", "")
        err_str: str = "{} {}: error for ".format(response_status_code, error_msg)
        err_str += ", ".join("=".join((str(k), str(v))) for k, v in kwargs.items())
        raise APIException(err_str)


def add_jikan_metadata(
    response: Union[requests.Response, aiohttp.ClientResponse],
    response_dict: Dict[str, Any],
    url: str,
) -> Dict[str, Any]:
    """Adds the response headers and jikan endpoint url to response dictionary"""
    response_dict["jikan_url"] = url
    # dict() is to convert from CIMultiDict[str, Any]Proxy for aiohttp.ClientResponse
    response_dict["headers"] = dict(response.headers)
    return response_dict


def get_url_with_page(url: str, page: Optional[int], delimiter: str = "/") -> str:
    """Add page to URL if it exists"""
    return url if page is None else f"{url}{delimiter}{page}"


def get_main_url(
    base_url: str, endpoint: str, id: int, extension: Optional[str], page: Optional[int]
) -> str:
    """Create URL for anime, manga, character, person, and club endpoints"""
    url = f"{base_url}/{endpoint}/{id}"
    if extension is not None:
        url += f"/{extension}"
        url = get_url_with_page(url, page)
    return url


def get_creator_url(
    base_url: str, creator_type: str, creator_id: int, page: Optional[int]
) -> str:
    """Create URL for producer and magazine endpoints"""
    url = f"{base_url}/{creator_type}/{creator_id}"
    return get_url_with_page(url, page)


def get_search_url(
    base_url: str,
    search_type: str,
    query: str,
    page: Optional[int],
    parameters: Optional[Mapping[str, Optional[Union[int, str, float]]]],
) -> str:
    """Create URL for search endpoint"""
    url = f"{base_url}/search/{search_type}?q={query}"
    url = get_url_with_page(url, page, delimiter="&page=")
    if parameters is not None:
        url += "".join(f"&{k}={v}" for k, v in parameters.items())
    return url


def get_season_url(base_url: str, year: int, season: str) -> str:
    """Create URL for season endpoint"""
    return f"{base_url}/season/{year}/{season.lower()}"


def get_schedule_url(base_url: str, day: Optional[str]) -> str:
    """Create URL for schedule endpoint"""
    base_schedule_url = f"{base_url}/schedule"
    return base_schedule_url if day is None else f"{base_schedule_url}/{day.lower()}"


def get_season_archive_url(base_url: str) -> str:
    """Create URL for season archive endpoint"""
    return f"{base_url}/season/archive"


def get_season_later_url(base_url: str) -> str:
    """Create URL for season later endpoint"""
    return f"{base_url}/season/later"


def get_top_url(
    base_url: str, type: str, page: Optional[int], subtype: Optional[str]
) -> str:
    """Create URL for top endpoint"""
    url = f"{base_url}/top/{type.lower()}"
    url = get_url_with_page(url, page)
    return url if subtype is None else f"{url}/{subtype.lower()}"


def get_genre_url(base_url: str, type: str, genre_id: int, page: Optional[int]) -> str:
    """Create URL for genre endpoint"""
    url = f"{base_url}/genre/{type.lower()}/{genre_id}"
    return get_url_with_page(url, page)


def get_user_url(
    base_url: str,
    username: str,
    request: Optional[str],
    argument: Optional[Union[int, str]],
    page: Optional[int],
    parameters: Optional[Mapping[str, Any]],
) -> str:
    """Create URL for user endpoint"""
    url = f"{base_url}/user/{username.lower()}"
    if request is not None:
        url += f"/{request}"
        if argument is not None:
            url += f"/{argument}"
        url = get_url_with_page(url, page)
    if parameters is not None:
        param_str = "&".join(f"{k}={v}" for k, v in parameters.items())
        url += f"?{param_str}"
    return url


def get_meta_url(
    base_url: str,
    request: str,
    type: Optional[str],
    period: Optional[str],
    offset: Optional[int],
) -> str:
    """Create URL for meta endpoint"""
    url = f"{base_url}/meta/{request}"
    if type is not None and period is not None:
        url += f"/{type}/{period}"
    return get_url_with_page(url, offset)
