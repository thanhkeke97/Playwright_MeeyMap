"""Configuration management - loads environment settings from ui.yaml."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class EnvConfig:
    """Represents one environment block from ui.yaml."""
    browser: str = "chromium"
    headless: bool = False
    url: str = ""
    username: str = ""
    password: str = ""
    wait_timeout: int = 3  # seconds
    short_time: int = 1
    retry: int = 5
    language: str = "Vi"
    url_api_meey_id: str = ""
    url_api_meey_land: str = ""
    url_api_meey_admin: str = ""
    url_api_meey_map: str = ""
    password_api: str = ""
    video_dir: str = "../result/video"
    trace_dir: str = "../result/trace"


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent / "playwright_tests"  # meeymaps-automation
_CONFIG_PATH = _PROJECT_ROOT / "config" / "ui.yaml"


def load_env_config(env: str = "stg") -> EnvConfig:
    """Load configuration for the given environment from ui.yaml."""
    env = os.environ.get("TEST_ENV", env)
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        all_config: dict[str, Any] = yaml.safe_load(f)

    raw = all_config.get(env, {})
    return EnvConfig(
        browser=raw.get("browser", "chromium"),
        headless=raw.get("headless_browser", False),
        url=raw.get("url", ""),
        username=str(raw.get("username", "")).strip(),
        password=str(raw.get("password", "")).strip(),
        wait_timeout=int(raw.get("wait_timeout", 3)),
        short_time=int(raw.get("short_time", 1)),
        retry=int(raw.get("retry", 5)),
        language=raw.get("language", "Vi"),
        url_api_meey_id=str(raw.get("url_api_meey_id", "")).strip(),
        url_api_meey_land=str(raw.get("url_api_meey_land", "")).strip(),
        url_api_meey_admin=str(raw.get("url_api_meey_admin", "")).strip(),
        url_api_meey_map=str(raw.get("url_api_meey_map", "")).strip(),
        password_api=str(raw.get("PASSWORD_API", "")).strip(),
        video_dir=str(raw.get("VIDEO_DIR", "../result/video")).strip(),
        trace_dir=str(raw.get("TRACE_DIR", "../result/trace")).strip(),
    )


def get_project_root() -> Path:
    return _PROJECT_ROOT


def get_thresh_hold(test_name: str) -> list[float]:
    """Load threshold values for a test from thresh_hold.json."""
    import json
    thresh_path = _PROJECT_ROOT / "config" / "thresh_hold.json"
    with open(thresh_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(test_name, [])
