"""
Map (Bản đồ quy hoạch) page object.
Converted from common_Ban_Do_QH_screen.robot locators + keywords/common/ban_do_qh.robot.
"""
from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import Page

from .base_page import BasePage


class MapPage(BasePage):
    """Page object for the map / planning lookup page."""

    # ══════════════════════════════════════════════════════════════════════════
    #  LOCATORS - Converted from common_Ban_Do_QH_screen.robot
    # ══════════════════════════════════════════════════════════════════════════

    # ── Tabs quy hoạch ──
    TAB_QUY_HOACH_XAY_DUNG = "//div[@class='map position-relative']//span[text()='Quy hoạch xây dựng']"
    TAB_QUY_HOACH_SU_DUNG_DAT = "//div[@class='map position-relative']//span[text()='Quy hoạch sử dụng đất']"
    TAB_KE_HOACH_SU_DUNG_DAT = "//div[@class='map position-relative']//span[text()='Kế hoạch sử dụng đất']"

    # ── Search box ──
    SEARCH_BOX_TIM_KIEM_O_DAT = "//div[@id='navbar-top']//span[text()='Tìm kiếm ô đất']"
    INPUT_SEARCH = "//input[@id='searchLocationInput']"
    KET_QUA_DAU_TIEN = '(//div[@class="location-list"]//div[@class="item-address"])[1]'
    ICON_XOA_TIM_KIEM = '//div[@class="search-container"]//img[@class="icon icon-delete-suggest"]'

    # ── Popup tìm kiếm ô đất - Tab ──
    TAB_TO_THUA = "//section[@class='search-top-action-ui-2']//div[text()='Tờ thửa']"
    TAB_GOC_RANH = "//section[@class='search-top-action-ui-2']//div[text()='Góc ranh']"
    TAB_KHU_VUC = "//section[@class='search-top-action-ui-2']//div[text()='Khu vực']"

    # ── Tab Tờ Thửa ──
    TO_THUA_INPUT_THUA_DAT_SO = "//label[contains(text(),'Thửa đất số')]//..//input"
    TO_THUA_INPUT_TO_BAN_DO_SO = "//label[contains(text(),'Tờ bản đồ số')]//..//input"
    TO_THUA_DROPDOWN_TINH_THANH_PHO = "//span[contains(text(),'Chọn Tỉnh/Thành phố')]"
    TO_THUA_INPUT_TINH_THANH_PHO = '//div[@id="province"]//input[@placeholder="Tìm kiếm"]'
    TO_THUA_DROPDOWN_QUAN_HUYEN = "//span[contains(text(),'Chọn Quận/Huyện')]"
    TO_THUA_INPUT_QUAN_HUYEN = '//div[@id="district"]//input[@placeholder="Tìm kiếm"]'
    TO_THUA_DROPDOWN_PHUONG_XA = "//span[contains(text(),'Chọn Phường/Xã')]"
    TO_THUA_INPUT_PHUONG_XA = '//div[@id="ward"]//input[@placeholder="Tìm kiếm"]'
    BUTTON_TRA_CUU_TREN_BAN_DO = "//button[normalize-space()='Tra cứu trên bản đồ']"
    LOADING_DANG_TIM_KIEM = "//section[@id='loading']//h2[text()='Đang tìm kiếm ô đất']"

    @staticmethod
    def to_thua_select_search_item(item_name: str) -> str:
        return f"//a[text()='{item_name}']"

    # ── Tab Góc Ranh ──
    GOC_RANH_UPLOAD_INPUT = '//input[@type="file"]'
    GOC_RANH_POPUP_XEM_LAI_ANH = "//label[text()='Xem lại ảnh']"
    GOC_RANH_BUTTON_DOC_DU_LIEU = "//button[contains(text(),'Đọc dữ liệu')]"
    GOC_RANH_DROPDOWN_TINH_THANH_PHO = "//span[contains(text(),'Chọn Tỉnh/Thành phố')]"
    GOC_RANH_BUTTON_TRA_CUU = "//button[contains(text(),'Tra cứu trên bản đồ')]"

    @staticmethod
    def goc_ranh_select_tinh_thanh_pho(name: str) -> str:
        return f"//span[text()='{name}']"

    # ── Popup điều hướng đăng nhập ──
    POPUP_DIEU_HUONG_BUTTON_CLOSE_CHUA_LOGIN = (
        '//div[@id="address-info"]//*[local-name()="svg"]/*[local-name()="path" '
        "and @d='M8.55806 8.55806C8.80214 8.31398 9.19786 8.31398 9.44194 8.55806L14 "
        "13.1161L18.5581 8.55806C18.8021 8.31398 19.1979 8.31398 19.4419 8.55806C19.686 "
        "8.80214 19.686 9.19786 19.4419 9.44194L14.8839 14L19.4419 18.5581C19.686 18.8021 "
        "19.686 19.1979 19.4419 19.4419C19.1979 19.686 18.8021 19.686 18.5581 19.4419L14 "
        "14.8839L9.44194 19.4419C9.19786 19.686 8.80214 19.686 8.55806 19.4419C8.31398 "
        "19.1979 8.31398 18.8021 8.55806 18.5581L13.1161 14L8.55806 9.44194C8.31398 "
        "9.19786 8.31398 8.80214 8.55806 8.55806Z']"
    )
    POPUP_DIA_CHI_CHI_TIET = "//div[@id='address-info']//div[@class='detail']//span[@class='main-text']"
    POPUP_DIA_CHI_PHUONG_XA = '//div[@id="address-info"]//div[@class="detail"]//div[@class="second-text"]'
    POPUP_BADGE_DO_PHU = "//div[@class='badge tooltip-trigger']"
    POPUP_BUTTON_XEM_CHI_TIET_QH = "//div[@class='xem-quy-hoach']//button[text()='Xem chi tiết quy hoạch']"
    POPUP_SHARE_ICON = "//div[@class='share icon']"
    POPUP_BUTTON_CLOSE = '//div[@class="close"]'
    POPUP_ICON_CHI_DUONG = '//div[@id="address-info"]//div[@class="menu-item"]//span[text()="Chỉ đường"]'
    POPUP_ICON_TIEN_ICH = '//div[@id="address-info"]//div[@class="menu-item"]//span[text()="Tiện ích"]'
    POPUP_ICON_TIN_DANG = '//div[@id="address-info"]//div[@class="menu-item"]//span[text()="Tin đăng"]'
    POPUP_CANH_BAO_CHUA_CO_DU_LIEU_QHSD_DAT = '//div[@id="address-info"]//span[text()="Chưa có dữ liệu QH sử dụng đất"]'
    POPUP_LINK_XEM_DS_KHU_VUC_CO_DU_LIEU = '//div[@id="address-info"]//span[text()="Xem danh sách khu vực có dữ liệu"]'
    POPUP_TONG_DIEN_TICH = "//div[contains(text(),'Tổng diện tích:')]"
    POPUP_LINK_KE_HOACH_SU_DUNG_DAT = '//div[@id="address-info"]//span[text()="Kế hoạch sử dụng đất của vị trí này"]'

    # ── Popup chi tiết quy hoạch sử dụng đất ──
    POPUP_CHI_TIET_TOP_CORNER = '//section[@id="top-corner"]'
    POPUP_CHI_TIET_DIA_CHI = '//section[@id="top-corner"]//h3[@class="location-address"]'
    POPUP_CHI_TIET_DIA_CHI_CHI_TIET = '//section[@id="top-corner"]//div[@class="location-subaddress"]'
    POPUP_CHI_TIET_TOA_DO = "//p[@class='location-coordinates']//span[@class='toa_do']"
    POPUP_CHI_TIET_DIEN_TICH = "//p[@class='location-area']//span[@class='dt']"
    POPUP_CHI_TIET_SO_TO = "//p[@class='location-land-plot']//span[contains(text(),'Số tờ')]//span[@class='dt']"
    POPUP_CHI_TIET_SO_THUA = "//p[@class='location-land-plot']//span[contains(text(),'Số thửa')]//span[@class='dt']"
    POPUP_CHI_TIET_BUTTON_ZALO = '//div[@class="footer-plan-info"]//div[contains(@class,"btn-zalo")]'
    POPUP_CHI_TIET_BUTTON_SDT = '//div[@class="footer-plan-info"]//div[contains(@class,"phone-contact")]'
    POPUP_CHI_TIET_BUTTON_FEEDBACK = '//div[@class="footer-plan-info"]//div[contains(@class,"feedback")]'

    @staticmethod
    def popup_chi_tiet_button_tien_ich(name: str) -> str:
        return f"//div[contains(@class,'action-bar')]//span[normalize-space()='{name}']"

    POPUP_CHI_TIET_THONG_TIN_DO_AN = "//h2[contains(text(),'Thông tin đồ án, quyết định')]//..//div[@class='info']"

    # ══════════════════════════════════════════════════════════════════════════
    #  HIGH-LEVEL ACTIONS - Converted from keywords/common/ban_do_qh.robot
    # ══════════════════════════════════════════════════════════════════════════

    def click_quy_hoach_su_dung_dat_tab(self):
        self.click_element(self.TAB_QUY_HOACH_SU_DUNG_DAT)

    def click_search_box(self):
        self.click_element(self.SEARCH_BOX_TIM_KIEM_O_DAT)

    def input_search(self, text: str, verify: bool = False):
        self.input_text(self.INPUT_SEARCH, text, clear=True)

    def click_first_result(self):
        self.click_element(self.KET_QUA_DAU_TIEN)

    def search_with_retry(self, address: str):
        """Tim kiem voi retry - nhập địa chỉ và retry nếu chưa thấy kết quả."""
        self.input_search(address)
        if not self.is_visible(self.KET_QUA_DAU_TIEN, timeout=5000):
            self.input_search(address)

    # ── Tab Tờ Thửa ──

    def select_tab_to_thua(self):
        self.click_element(self.TAB_TO_THUA)

    def input_thua_dat_so(self, value: str):
        self.input_text(self.TO_THUA_INPUT_THUA_DAT_SO, value)

    def input_to_ban_do_so(self, value: str):
        self.input_text(self.TO_THUA_INPUT_TO_BAN_DO_SO, value)

    def select_tinh_thanh_pho(self, name: str):
        self.click_element(self.TO_THUA_DROPDOWN_TINH_THANH_PHO)
        self.input_text(self.TO_THUA_INPUT_TINH_THANH_PHO, name)
        self.click_element(self.to_thua_select_search_item(name))

    def select_quan_huyen(self, name: str):
        self.click_element(self.TO_THUA_DROPDOWN_QUAN_HUYEN)
        self.input_text(self.TO_THUA_INPUT_QUAN_HUYEN, name)
        self.click_element(self.to_thua_select_search_item(name))

    def select_phuong_xa(self, name: str):
        self.click_element(self.TO_THUA_DROPDOWN_PHUONG_XA)
        self.input_text(self.TO_THUA_INPUT_PHUONG_XA, name)
        self.click_element(self.to_thua_select_search_item(name))

    def click_tra_cuu_tren_ban_do(self):
        self.click_element(self.BUTTON_TRA_CUU_TREN_BAN_DO)

    def wait_loading_tim_kiem_disappear(self, visible_timeout: int = 2000, hidden_timeout: int = 20_000):
        """Chờ loading 'Đang tìm kiếm ô đất' biến mất."""
        try:
            self.page.locator(self.LOADING_DANG_TIM_KIEM).wait_for(
                state="visible", timeout=visible_timeout
            )
        except Exception:
            pass
        try:
            self.page.locator(self.LOADING_DANG_TIM_KIEM).wait_for(
                state="hidden", timeout=hidden_timeout
            )
        except Exception:
            pass

    # ── Tab Góc Ranh ──

    def select_tab_goc_ranh(self):
        self.click_element(self.TAB_GOC_RANH)

    def upload_anh_goc_ranh(self, files: list[str]):
        self.upload_files(self.GOC_RANH_UPLOAD_INPUT, files)

    def wait_popup_xem_lai_anh(self, timeout: int = 20_000):
        self.wait_visible(self.GOC_RANH_POPUP_XEM_LAI_ANH, timeout=timeout)

    def click_doc_du_lieu(self):
        self.click_element(self.GOC_RANH_BUTTON_DOC_DU_LIEU)

    def goc_ranh_select_tinh_thanh_pho_dropdown(self, is_wait_visible: bool = False):
        if is_wait_visible:
            self.wait_visible(self.GOC_RANH_DROPDOWN_TINH_THANH_PHO, timeout=20_000)
        self.click_element(self.GOC_RANH_DROPDOWN_TINH_THANH_PHO)

    def goc_ranh_select_thanh_pho(self, name: str):
        self.click_element(self.goc_ranh_select_tinh_thanh_pho(name))

    def goc_ranh_click_tra_cuu(self):
        self.click_element(self.GOC_RANH_BUTTON_TRA_CUU)

    # ── Popup điều hướng / thông tin ô đất ──

    def close_popup_dieu_huong(self):
        """Đóng popup điều hướng đăng nhập (nút X SVG)."""
        self.click_element(self.POPUP_DIEU_HUONG_BUTTON_CLOSE_CHUA_LOGIN)

    def click_xem_chi_tiet_quy_hoach(self):
        self.click_element(self.POPUP_BUTTON_XEM_CHI_TIET_QH)

    def click_on_map(self, x: int, y: int):
        """Click vào vị trí (x, y) trên body."""
        self.page.locator("body").click(position={"x": x, "y": y}, force=True)
