"""
Login page object.
Converted from common_Login_screen.robot + keywords/common/login_action.robot.
"""
from __future__ import annotations

from playwright.sync_api import Page

from .base_page import BasePage


class LoginPage(BasePage):
    """Login & authentication related actions."""

    # ── Locators ────────────────────────────────────────────────────────────

    POPUP_DANG_KY_DANG_NHAP = "//div[text()=' Đăng nhập hoặc tạo tài khoản ']"
    BUTTON_CLOSE_FORM = '//button[@data-key="closeForm"]'
    INPUT_SO_DIEN_THOAI = '//input[@placeholder="Nhập Số điện thoại hoặc Email"]'
    INPUT_PASSWORD = '//input[@type="password"]'
    BUTTON_TIEP_TUC = '//button[normalize-space()="Tiếp tục"]'
    BUTTON_DANG_NHAP = '//button[normalize-space()="Đăng nhập"]'
    AVATAR_TEXT = '//div[contains(@class,"avatar")]'
    POPUP_MEEYID = '//div[@data-enter="loginWithPhoneOrEmail"]'

    # ── Actions ─────────────────────────────────────────────────────────────

    def open_login_popup(self):
        """Mở popup đăng ký/đăng nhập."""
        # Click button đăng nhập trên header
        btn = '//div[contains(@class,"btn-login")]'
        self.click_element(btn)
        self.wait_visible(self.POPUP_DANG_KY_DANG_NHAP, timeout=20_000)

    def login(self, username: str, password: str):
        """Full login flow."""
        self.open_login_popup()
        self.input_text(self.INPUT_SO_DIEN_THOAI, username)
        self.click_element(self.BUTTON_TIEP_TUC)
        self.page.locator(self.INPUT_PASSWORD).first.click()
        self.input_text(self.INPUT_PASSWORD, password)
        self.click_element(self.BUTTON_DANG_NHAP)
        self.wait_visible(self.AVATAR_TEXT, timeout=20_000)

    def close_login_form(self):
        self.click_element(self.BUTTON_CLOSE_FORM)
