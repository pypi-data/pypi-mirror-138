import os
from typing import Optional
from zoneinfo import ZoneInfo

import httpx
import yaml
from dateutil import parser
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

OWNER = os.getenv("OWNER", None)
TOKEN = os.getenv("EXPIRING_TOKEN", None)
REPO = os.getenv("REPOSITORY", None)
BASE = "https://api.github.com/repos"
URL = f"{BASE}/{OWNER}/{REPO}/contents/justices/list.yaml"
HEADERS = {
    "Authorization": f"token {TOKEN}",  # bearer
    "Accept": "application/vnd.github.VERSION.raw",  # raw file
}


def get_justice_list_url() -> Optional[str]:
    """Gets the proper URL if environment variables are set

    Returns:
        Optional[str]: URL string

    >>> from lawsql_cases_justices import get_justice_list_url
    >>> assert URL == get_justice_list_url()
    True
    """
    return URL if all([OWNER, TOKEN, REPO]) else None


def get_justice_api_response() -> Optional[httpx.Response]:
    """Assumes the existence of a valid URL to secure the response object.

    Returns:
        Optional[httpx.Response]: The response object consisting of byte data from the yaml file online

    >>> from lawsql_cases_justices import get_justice_api_response
    >>> r = get_justice_api_response()
    >>> r
    <Response [200 OK]>
    """
    if not (url := get_justice_list_url()):
        return None
    with httpx.Client() as client:
        return client.get(url, headers=HEADERS)


def get_justice_data() -> Optional[dict]:
    """With properly set .env values, get the updated list of justices.

    Returns:
        Optional[dict]: [description]

    >>> from lawsql_cases_justices import get_justice_data
    >>> data = get_justice_data()
    >>> assert isinstance(data, dict)
    True
    >>> assert data.keys() == dict_keys(['last_modified', 'justices'])
    True
    >>> import datetime
    >>> assert isinstance(data['last_modified'], datetime.datetime)
    True
    >>> assert isinstance(data['justices'], list)
    True
    """
    from .config import get_justice_from_dict

    r = get_justice_api_response()
    if not r:
        return None

    return {
        "last_modified": parser.parse(r.headers["last-modified"]).astimezone(
            ZoneInfo("Asia/Manila")
        ),
        "justices": [
            get_justice_from_dict(i)
            for i in yaml.load(r.content, Loader=yaml.FullLoader)
        ],
    }
