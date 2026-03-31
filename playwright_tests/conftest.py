"""
Pytest conftest.py - replaces global.robot Suite/Test Setup/Teardown.
Provides fixtures for browser, page, page objects, and YOLO engine.
"""
from __future__ import annotations

import os
import sys
import shutil
import time
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from config.settings import load_env_config, get_project_root, EnvConfig
from core.auth_helper import get_bearer_token_and_cookies, build_auth_cookie_value
from core.yolo_template_search import YOLOTemplateSearch
from pages.map_page import MapPage
from pages.login_page import LoginPage


# ══════════════════════════════════════════════════════════════════════════════
#  Session-scoped fixtures
# ══════════════════════════════════════════════════════════════════════════════

def pytest_addoption(parser):
    """Custom CLI options for the Playwright test project."""
    parser.addoption(
        "--env",
        action="store",
        default=os.environ.get("TEST_ENV", "stg"),
        help="Target environment from config/ui.yaml (e.g. dev, stg, prod)",
    )

@pytest.fixture(scope="session")
def env_config(pytestconfig) -> EnvConfig:
    """Load environment configuration once per session."""
    env = pytestconfig.getoption("env")
    return load_env_config(env)


@pytest.fixture(scope="session")
def project_root() -> Path:
    return get_project_root()


@pytest.fixture(scope="session")
def screenshot_dir(project_root: Path) -> Path:
    d = project_root / "results" / "ui" / "screenshots"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def video_dir(project_root: Path) -> Path:
    d = project_root / "results" / "ui" / "videos"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def yolo_engine(project_root: Path) -> YOLOTemplateSearch:
    """Initialize YOLO engine once per session."""
    model_path = str(project_root / "yolo11n.pt")
    thresh_path = str(project_root / "config" / "thresh_hold.json")
    return YOLOTemplateSearch(model_path=model_path, thresh_hold_path=thresh_path)


@pytest.fixture(scope="session")
def auth_tokens(env_config: EnvConfig) -> tuple[str, str, int]:
    """Get auth tokens once per session."""
    return get_bearer_token_and_cookies(
        api_base_url=env_config.url_api_meey_id,
        phone_number=env_config.username,
        password=env_config.password,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Test-scoped fixtures (new browser per test)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def playwright_instance():
    """Provide a raw Playwright instance."""
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright_instance, env_config: EnvConfig, pytestconfig) -> Browser:
    """Launch browser - one per test."""
    launch_opts = {"headless": False if pytestconfig.getoption("headed", default=False) else env_config.headless}
    browser = playwright_instance.chromium.launch(**launch_opts)
    yield browser
    browser.close()


@pytest.fixture
def context(
    browser: Browser,
    env_config: EnvConfig,
    video_dir: Path,
    request,
) -> BrowserContext:
    """Create browser context with video recording and permissions."""
    test_name = request.node.name
    test_video_dir = video_dir / test_name
    test_video_dir.mkdir(parents=True, exist_ok=True)

    ctx = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=str(test_video_dir),
        permissions=["geolocation"],
    )
    ctx.set_default_timeout(30_000)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Create new page."""
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture
def page_with_cookie(
    context: BrowserContext,
    env_config: EnvConfig,
    auth_tokens: tuple[str, str, int],
) -> Page:
    """
    Create page, navigate to map, inject _auth cookie, reload.
    Replaces Robot keyword: Before Test Login With Cookie
    """
    p = context.new_page()
    # Handle dialogs
    p.on("dialog", lambda d: d.dismiss())

    # Navigate to map
    url = env_config.url
    p.goto(f"{url}tra-cuu-quy-hoach")

    # Inject auth cookie
    refresh_token, access_token, expires_in = auth_tokens
    cookie_value = build_auth_cookie_value(access_token, refresh_token, expires_in)
    from urllib.parse import urlparse
    parsed = urlparse(url)
    context.add_cookies([{
        "name": "_auth",
        "value": cookie_value,
        "domain": parsed.hostname,
        "path": "/",
    }])
    p.reload()
    time.sleep(1)

    # Close popups if any
    try:
        popup_close = "(//div[@class='modal-content']//*[contains(@class,'close')])[1]"
        if p.locator(popup_close).first.is_visible(timeout=5000):
            p.locator(popup_close).first.click()
    except Exception:
        pass

    yield p
    p.close()


# ══════════════════════════════════════════════════════════════════════════════
#  Page Object fixtures
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def map_page(page_with_cookie: Page, env_config: EnvConfig) -> MapPage:
    """MapPage object with authenticated page."""
    return MapPage(page_with_cookie, wait_timeout=env_config.wait_timeout)


@pytest.fixture
def login_page(page: Page, env_config: EnvConfig) -> LoginPage:
    """LoginPage object."""
    return LoginPage(page, wait_timeout=env_config.wait_timeout)
