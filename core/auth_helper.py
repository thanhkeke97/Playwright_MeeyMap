"""
Authentication helper - handles API login and cookie injection.
Replaces: keywords/api/authentication.robot + core/api/api_access.robot Refresh Cookie
"""
from __future__ import annotations

import json
import urllib.parse

import requests


DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "X-CLIENT-ID": "meeyland",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def get_bearer_token_and_cookies(
    api_base_url: str,
    phone_number: str,
    password: str,
) -> tuple[str, str, int]:
    """
    Get refresh_token, access_token, expires_in via MeeyID API.
    Replaces Robot keyword: API Get BearerToken&Cookies
    """
    session = requests.Session()
    session.verify = True
    session.headers.update(DEFAULT_HEADERS)

    login_payload = {
        "target": phone_number,
        "type": "phone",
        "refCode": "",
        "provider": "zns",
    }

    # Step 1: Request login
    resp1 = session.post(
        f"{api_base_url}/auth/api/login",
        data=json.dumps(login_payload, separators=(",", ":")),
        timeout=30,
    )
    resp1.raise_for_status()
    data1 = resp1.json()
    request_id = data1["data"]["requestId"]

    confirm_payload = {
        "requestId": request_id,
        "password": password,
    }

    # Step 2: Confirm password
    resp2 = session.post(
        f"{api_base_url}/auth/api/confirm-password",
        data=json.dumps(confirm_payload, separators=(",", ":")),
        timeout=30,
    )
    resp2.raise_for_status()
    data2 = resp2.json()
    refresh_token = data2["data"]["refresh_token"]
    access_token = data2["data"]["access_token"]
    expires_in = data2["data"]["expires_in"]

    return refresh_token, access_token, expires_in


def build_auth_cookie_value(
    access_token: str, refresh_token: str, expires_in: int
) -> str:
    """Build URL-encoded _auth cookie value."""
    raw = json.dumps({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
    }, separators=(",", ":"))
    return urllib.parse.quote(raw, safe="")
