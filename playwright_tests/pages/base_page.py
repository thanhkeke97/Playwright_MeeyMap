"""
Base page object - common operations shared across all pages.
Converted from core/common/utils.robot MEEY keywords.
"""
from __future__ import annotations

import time
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, wait_timeout: int = 3):
        self.page = page
        self.wait_timeout = wait_timeout * 1000  # convert seconds -> ms

    # ── Helpers tương ứng MEEY keywords ─────────────────────────────────────

    def click_element(self, selector: str, timeout: int | None = None):
        """MEEY Click Element"""
        t = timeout or self.wait_timeout
        self.page.locator(selector).first.click(timeout=t)

    def click_element_js(self, selector: str):
        """MEEY Click Element JS - click via JavaScript."""
        self.page.eval_on_selector(selector, "el => el.click()")

    def input_text(self, selector: str, text: str, clear: bool = True):
        """MEEY Input Text"""
        loc = self.page.locator(selector).first
        if clear:
            loc.fill(text)
        else:
            loc.type(text)

    def wait_visible(self, selector: str, timeout: int | None = None):
        """MEEY Wait Until Element Is Visible"""
        t = timeout or self.wait_timeout
        self.page.locator(selector).first.wait_for(state="visible", timeout=t)

    def wait_not_visible(self, selector: str, timeout: int | None = None):
        """MEEY Wait Until Element Is Not Visible"""
        t = timeout or self.wait_timeout
        self.page.locator(selector).first.wait_for(state="hidden", timeout=t)

    def wait_attached(self, selector: str, timeout: int | None = None):
        """Wait for element to be attached to DOM."""
        t = timeout or self.wait_timeout
        self.page.locator(selector).first.wait_for(state="attached", timeout=t)

    def get_text(self, selector: str) -> str:
        """Get text content of element."""
        return (self.page.locator(selector).first.text_content() or "").strip()

    def get_element_count(self, selector: str) -> int:
        """Get count of matching elements."""
        return self.page.locator(selector).count()

    def is_visible(self, selector: str, timeout: int = 2000) -> bool:
        """Check if element is visible within timeout."""
        try:
            self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def upload_files(self, selector: str, files: list[str]):
        """Upload files to a file input."""
        self.page.locator(selector).set_input_files(files)

    def close_all_popups(self):
        """Close all modal popups if present."""
        popup_selector = "(//div[@class='modal-content']//*[contains(@class,'close')])[1]"
        try:
            if self.is_visible(popup_selector, timeout=5000):
                self.click_element_js(popup_selector)
                time.sleep(0.5)
                self.close_all_popups()
        except Exception:
            print("✅ Không tìm thấy popup nào cần đóng")
