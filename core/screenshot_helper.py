"""Screenshot utility for Playwright pages."""
from __future__ import annotations

import os
import random
import string
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page


def _random_string(length: int = 20) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def take_screenshot(page: Page, screenshot_dir: str | Path, name: str | None = None) -> str:
    """Chụp screenshot và trả về đường dẫn file."""
    screenshot_dir = Path(screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    if name is None:
        name = f"screenshot_{_random_string()}"
    filepath = screenshot_dir / f"{name}.png"
    page.screenshot(path=str(filepath), full_page=False, timeout=25_000)
    print(f"✅ Screenshot: {filepath}")
    return str(filepath)


def wait_for_map_stable(
    page: Page,
    screenshot_dir: str | Path,
    yolo_engine,
    sleep_time: float = 1.0,
    max_retry: int = 15,
    min_template_threshold: float = 0.8,
) -> None:
    """Chờ bản đồ ổn định bằng cách so sánh 2 screenshot liên tiếp."""
    current_image = take_screenshot(page, screenshot_dir)
    for _ in range(max_retry):
        time.sleep(sleep_time)
        new_image = take_screenshot(page, screenshot_dir)
        result = yolo_engine.compare_full_screenshots(
            current_image,
            new_image,
            template_threshold=min_template_threshold,
            min_template_threshold=min_template_threshold,
        )
        if len(result) > 0:
            return
        current_image = new_image
    print("⚠️ Map chưa ổn định sau max retries")
