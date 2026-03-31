"""
Test: Tra cứu Quy hoạch Sử dụng đất - Login
Converted from: tests/ui/quy_hoach_su_dung_dat/Tra_Cuu_Quy_Hoach_Su_Dung_Dat_Login.robot

8 test cases covering:
  - Tìm kiếm địa chỉ ô đất có/không có dữ liệu quy hoạch
  - Click địa chỉ ô đất có/không có dữ liệu
  - Tìm kiếm theo tờ thửa, góc ranh
  - Kiểm tra button xem chi tiết quy hoạch
  - Kiểm tra nút X đóng popup
"""
from __future__ import annotations

import time
from pathlib import Path

import pytest

from config.settings import get_project_root, get_thresh_hold
from core.screenshot_helper import take_screenshot, wait_for_map_stable
from pages.map_page import MapPage


# Đường dẫn gốc cho test data hình ảnh
DATA_ROOT = get_project_root() / "resources" / "data_test" / "file_upload" / "quy_hoach_su_dung_dat" / "tra_cuu"

pytestmark = [pytest.mark.MAP, pytest.mark.QHSDD]


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 001: Tìm kiếm địa chỉ 1 ô đất có dữ liệu quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_001:
    """Kiểm tra ô đất có dữ liệu quy hoạch - tìm kiếm địa chỉ."""

    DIA_CHI = "16 Đường Trần Duy Hưng"
    DIA_CHI_CAP_THAP = "16 Đường Trần Duy Hưng"
    DIA_CHI_PHUONG_XA = "Trung Hoà, Yên Hòa, Hà Nội, Việt Nam"
    SMALL_IMAGE = str(DATA_ROOT / "QHSDD_TRA_CUU_LOGIN_001" / "QHSDD_TRA_CUU_LOGIN_001.png")
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_001"

    def test_tim_kiem_dia_chi_co_du_lieu(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        # Bước 1: Click tab Quy hoạch sử dụng đất
        mp.click_quy_hoach_su_dung_dat_tab()

        # Bước 2: Mở search box và tìm kiếm
        mp.click_search_box()
        mp.search_with_retry(self.DIA_CHI)
        mp.click_first_result()

        # Bước 3: Chờ bản đồ ổn định
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Bước 4: Chụp screenshot và so khớp ảnh mẫu
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.SMALL_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(result) == 1, f"⚠️ Không tìm thấy điểm đất trên bản đồ sau khi tìm kiếm địa chỉ: {self.DIA_CHI_CAP_THAP}"

        # Bước 5: Verify popup điều hướng đăng nhập
        mp.wait_visible(mp.POPUP_DIA_CHI_CHI_TIET, timeout=mp.wait_timeout)
        text_cap_thap = mp.get_text(mp.POPUP_DIA_CHI_CHI_TIET)
        assert text_cap_thap == self.DIA_CHI_CAP_THAP, f"⚠️ Địa chỉ hiển thị không đúng: {text_cap_thap}"

        text_phuong_xa = mp.get_text(mp.POPUP_DIA_CHI_PHUONG_XA)
        assert self.DIA_CHI_PHUONG_XA in text_phuong_xa, f"⚠️ Địa chỉ phường xã không đúng: {text_phuong_xa}"

        # Bước 6: Verify các element trong popup
        mp.wait_visible(mp.POPUP_BADGE_DO_PHU, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_SHARE_ICON, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_BUTTON_XEM_CHI_TIET_QH, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_BUTTON_CLOSE, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_ICON_CHI_DUONG, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_ICON_TIEN_ICH, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_ICON_TIN_DANG, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_TONG_DIEN_TICH, timeout=mp.wait_timeout)


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 002: Click địa chỉ 1 ô đất có dữ liệu quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_002:
    """Kiểm tra ô đất có dữ liệu quy hoạch - click địa chỉ."""

    DIA_CHI = "Đường Trần Duy Hưng, Trung Hoà, Cầu Giấy, Hà Nội, Việt Nam"
    DIA_CHI_CAP_THAP = "17 T1"
    DIA_CHI_PHUONG_XA = "17T1 P. Hoàng Đạo Thúy, Trung Hoà, Yên Hòa, Hà Nội, Vietnam"
    CLICK_IMAGE = str(DATA_ROOT / "QHSDD_TRA_CUU_LOGIN_002" / "QHSDD_TRA_CUU_LOGIN_002.png")
    SMALL_IMAGE = str(DATA_ROOT / "QHSDD_TRA_CUU_LOGIN_002" / "QHSDD_TRA_CUU_LOGIN_0021.png")
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_002"

    def test_click_dia_chi_co_du_lieu(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.search_with_retry(self.DIA_CHI)
        mp.click_first_result()
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Lấy tọa độ ảnh mẫu và click trên bản đồ
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        click_result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.CLICK_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(click_result) >= 1, "⚠️ Không tìm thấy vị trí click trên bản đồ"
        x, y = click_result[0]
        mp.click_on_map(x, y)
        time.sleep(1)
        # Verify sau khi click
        screenshot_path2 = take_screenshot(mp.page, screenshot_dir)
        result = yolo_engine.find_small_image_in_large(
            screenshot_path2, self.SMALL_IMAGE,
            min_template_threshold=thresh_hold[1] if len(thresh_hold) > 1 else 0.1,
        )
        assert len(result) == 1, f"⚠️ Không tìm thấy điểm đất: {self.DIA_CHI_CAP_THAP}"

        # Verify popup
        mp.wait_visible(mp.POPUP_DIA_CHI_CHI_TIET, timeout=mp.wait_timeout)
        assert mp.get_text(mp.POPUP_DIA_CHI_CHI_TIET) == self.DIA_CHI_CAP_THAP
        assert self.DIA_CHI_PHUONG_XA in mp.get_text(mp.POPUP_DIA_CHI_PHUONG_XA)

        mp.wait_visible(mp.POPUP_BADGE_DO_PHU, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_SHARE_ICON, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_BUTTON_XEM_CHI_TIET_QH, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_BUTTON_CLOSE, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_ICON_CHI_DUONG, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_ICON_TIEN_ICH, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_ICON_TIN_DANG, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_TONG_DIEN_TICH, timeout=mp.wait_timeout)


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 003: Tìm kiếm theo tờ thửa có dữ liệu quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_003:
    """Tìm kiếm theo tờ thửa có dữ liệu quy hoạch."""

    THUA_DAT_SO = "50"
    TO_BAN_DO_SO = "32"
    THANH_PHO = "Hà Nội"
    QUAN_HUYEN = "Đống Đa"
    PHUONG_XA = "Kim Liên"
    SMALL_IMAGE = str(DATA_ROOT / "QHSDD_TRA_CUU_LOGIN_003" / "QHSDD_TRA_CUU_LOGIN_003.png")
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_003"

    def test_tim_kiem_to_thua(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.select_tab_to_thua()

        # Nhập thông tin tờ thửa
        mp.input_thua_dat_so(self.THUA_DAT_SO)
        mp.input_to_ban_do_so(self.TO_BAN_DO_SO)
        mp.select_tinh_thanh_pho(self.THANH_PHO)
        mp.select_quan_huyen(self.QUAN_HUYEN)
        mp.select_phuong_xa(self.PHUONG_XA)

        # Tra cứu
        mp.click_tra_cuu_tren_ban_do()
        mp.wait_loading_tim_kiem_disappear(visible_timeout=2000)
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Verify
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.SMALL_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(result) == 1, (
            f"⚠️ Không tìm thấy điểm đất: Thửa {self.THUA_DAT_SO}, Tờ {self.TO_BAN_DO_SO}, "
            f"{self.PHUONG_XA}, {self.QUAN_HUYEN}, {self.THANH_PHO}"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 004: Tìm kiếm theo góc ranh có dữ liệu quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_004:
    """Tìm kiếm theo góc ranh có dữ liệu quy hoạch."""

    THANH_PHO = "Hồ Chí Minh"
    SMALL_IMAGE = str(DATA_ROOT / "QHSDD_TRA_CUU_LOGIN_004" / "QHSDD_TRA_CUU_LOGIN_004.png")
    IMAGE_GOC_RANH = str(
        get_project_root() / "resources" / "data_test" / "file_upload" / "login"
        / "QHXD_LOGIN_03" / "Goc_Ranh.jpeg"
    )
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_004"

    def test_tim_kiem_goc_ranh(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.select_tab_goc_ranh()

        # Upload ảnh góc ranh
        mp.upload_anh_goc_ranh([self.IMAGE_GOC_RANH])
        mp.wait_popup_xem_lai_anh()
        mp.click_doc_du_lieu()

        # Chọn tỉnh/thành phố
        mp.goc_ranh_select_tinh_thanh_pho_dropdown(is_wait_visible=True)
        mp.goc_ranh_select_thanh_pho(self.THANH_PHO)
        mp.goc_ranh_click_tra_cuu()

        mp.wait_loading_tim_kiem_disappear(visible_timeout=2000)
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Verify
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.SMALL_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(result) == 1, f"⚠️ Không tìm thấy điểm đất khi tìm theo góc ranh, TP {self.THANH_PHO}"


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 005: Kiểm tra button xem chi tiết quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_005:
    """Kiểm tra button xem chi tiết quy hoạch."""

    DIA_CHI = "Tòa nhà A17, Phố Tạ Quang Bửu, Bách Khoa, Bạch Mai, Hà Nội, Việt Nam"
    DIA_CHI_ASSERT = "Tòa nhà A17"
    DIA_CHI_CHI_TIET_ASSERT = "Phố Tạ Quang Bửu,  Bách Khoa, Bạch Mai, Hà Nội, Việt Nam"
    TOA_DO_ASSERT = "21.003882, 105.847607"
    DIEN_TICH_ASSERT = "2,373.69 m²"
    SO_TO_ASSERT = "38"
    SO_THUA_ASSERT = "19"

    def test_button_xem_chi_tiet_quy_hoach(self, map_page: MapPage, yolo_engine, screenshot_dir):
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.search_with_retry(self.DIA_CHI)
        mp.click_first_result()
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Click button xem chi tiết (nếu visible)
        if mp.is_visible(mp.POPUP_BUTTON_XEM_CHI_TIET_QH, timeout=2000):
            mp.click_xem_chi_tiet_quy_hoach()

        # Verify popup chi tiết quy hoạch sử dụng đất
        mp.wait_visible(mp.POPUP_CHI_TIET_TOP_CORNER)

        # ── Assert thông tin địa chỉ, tọa độ, diện tích, số tờ, số thửa ──
        dia_chi_ui = mp.get_text(mp.POPUP_CHI_TIET_DIA_CHI)
        assert dia_chi_ui == self.DIA_CHI_ASSERT, (
            f"⚠️ Địa chỉ không đúng, kỳ vọng: {self.DIA_CHI_ASSERT}, thực tế: {dia_chi_ui}"
        )

        dia_chi_chi_tiet_ui = mp.get_text(mp.POPUP_CHI_TIET_DIA_CHI_CHI_TIET)
        dia_chi_chi_tiet_ui = dia_chi_chi_tiet_ui.replace("Độ phủ", "").strip()
        assert dia_chi_chi_tiet_ui == self.DIA_CHI_CHI_TIET_ASSERT, (
            f"⚠️ Địa chỉ chi tiết không đúng, kỳ vọng: {self.DIA_CHI_CHI_TIET_ASSERT}, thực tế: {dia_chi_chi_tiet_ui}"
        )

        toa_do_ui = mp.get_text(mp.POPUP_CHI_TIET_TOA_DO)
        assert toa_do_ui == self.TOA_DO_ASSERT, f"⚠️ Tọa độ không đúng: {toa_do_ui}"

        dien_tich_ui = mp.get_text(mp.POPUP_CHI_TIET_DIEN_TICH)
        assert dien_tich_ui == self.DIEN_TICH_ASSERT, f"⚠️ Diện tích không đúng: {dien_tich_ui}"

        so_to_ui = mp.get_text(mp.POPUP_CHI_TIET_SO_TO)
        assert so_to_ui == self.SO_TO_ASSERT, f"⚠️ Số tờ không đúng: {so_to_ui}"

        so_thua_ui = mp.get_text(mp.POPUP_CHI_TIET_SO_THUA)
        assert so_thua_ui == self.SO_THUA_ASSERT, f"⚠️ Số thửa không đúng: {so_thua_ui}"

        # ── Assert button tiện ích ──
        for tien_ich in ["Chỉ đường", "Tiện ích", "Tin đăng", "La bàn"]:
            loc = mp.popup_chi_tiet_button_tien_ich(tien_ich)
            mp.wait_visible(loc, timeout=mp.wait_timeout)

        # ── Assert thông tin đồ án, quyết định ──
        count = mp.get_element_count(mp.POPUP_CHI_TIET_THONG_TIN_DO_AN)
        assert count > 0, "⚠️ Không có thông tin đồ án, quyết định"

        # ── Assert footer ──
        mp.wait_visible(mp.POPUP_CHI_TIET_BUTTON_ZALO, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_CHI_TIET_BUTTON_SDT, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_CHI_TIET_BUTTON_FEEDBACK, timeout=mp.wait_timeout)


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 006: Tìm kiếm địa chỉ 1 ô đất KHÔNG có dữ liệu quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_006:
    """Tìm kiếm ô đất không có dữ liệu QH sử dụng đất."""

    DIA_CHI_KHONG_CO_DU_LIEU = "19.319819408313506, 105.18519408261909"
    DIA_CHI_CAP_THAP = "859P+X2X"
    DIA_CHI_PHUONG_XA = "Quy Hop, Quỳ Hợp District, Nghe An, Vietnam"
    SMALL_IMAGE = str(
        get_project_root() / "resources" / "data_test" / "file_upload"
        / "quy_hoach_su_dung_dat" / "tra_cuu" / "QHSDD_TRA_CUU_NO_LOGIN_006"
        / "QHSDD_TRA_CUU_NO_LOGIN_006.png"
    )
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_006"

    def test_tim_kiem_dia_chi_khong_co_du_lieu(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.input_search(self.DIA_CHI_KHONG_CO_DU_LIEU)
        mp.click_first_result()
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Verify ảnh mẫu
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.SMALL_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(result) == 1, f"⚠️ Không tìm thấy điểm đất: {self.DIA_CHI_KHONG_CO_DU_LIEU}"

        # Verify cảnh báo không có dữ liệu
        mp.wait_visible(mp.POPUP_CANH_BAO_CHUA_CO_DU_LIEU_QHSD_DAT, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_BADGE_DO_PHU, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_SHARE_ICON, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_LINK_KE_HOACH_SU_DUNG_DAT, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_LINK_XEM_DS_KHU_VUC_CO_DU_LIEU, timeout=mp.wait_timeout)


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 007: Click địa chỉ 1 ô đất KHÔNG có dữ liệu quy hoạch
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_007:
    """Click ô đất không có dữ liệu QH sử dụng đất."""

    DIA_CHI = "19.319819408313506, 105.18519408261909"
    DIA_CHI_CAP_THAP = "85CM+829"
    DIA_CHI_PHUONG_XA = "Unnamed, Road, Quỳ Hợp, Nghệ An, Vietnam"
    CLICK_IMAGE = str(
        get_project_root() / "resources" / "data_test" / "file_upload"
        / "quy_hoach_su_dung_dat" / "tra_cuu" / "QHSDD_TRA_CUU_NO_LOGIN_007"
        / "QHSDD_TRA_CUU_NO_LOGIN_007.png"
    )
    SMALL_IMAGE = str(
        get_project_root() / "resources" / "data_test" / "file_upload"
        / "quy_hoach_su_dung_dat" / "tra_cuu" / "QHSDD_TRA_CUU_NO_LOGIN_007"
        / "QHSDD_TRA_CUU_NO_LOGIN_0071.png"
    )
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_007"

    def test_click_dia_chi_khong_co_du_lieu(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.search_with_retry(self.DIA_CHI)
        mp.click_first_result()
        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Click trên bản đồ
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        click_result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.CLICK_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(click_result) >= 1, "⚠️ Không tìm thấy vị trí click"
        x, y = click_result[0]
        mp.click_on_map(x, y)
        time.sleep(1)

        # Verify sau click
        screenshot_path2 = take_screenshot(mp.page, screenshot_dir)
        result = yolo_engine.find_small_image_in_large(
            screenshot_path2, self.SMALL_IMAGE,
            min_template_threshold=thresh_hold[1] if len(thresh_hold) > 1 else 0.1,
        )
        assert len(result) == 1, f"⚠️ Không tìm thấy điểm đất: {self.DIA_CHI_CAP_THAP}"

        # Verify cảnh báo không có dữ liệu
        mp.wait_visible(mp.POPUP_CANH_BAO_CHUA_CO_DU_LIEU_QHSD_DAT, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_BADGE_DO_PHU, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_SHARE_ICON, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_LINK_KE_HOACH_SU_DUNG_DAT, timeout=mp.wait_timeout)
        mp.wait_visible(mp.POPUP_LINK_XEM_DS_KHU_VUC_CO_DU_LIEU, timeout=mp.wait_timeout)


# ══════════════════════════════════════════════════════════════════════════════
#  Test case 008: Kiểm tra nút X đóng popup khi không có dữ liệu
# ══════════════════════════════════════════════════════════════════════════════

class TestQHSDD_TRA_CUU_LOGIN_008:
    """Kiểm tra nút X đóng popup khi không có dữ liệu quy hoạch."""

    DIA_CHI = "19.319819408313506, 105.18519408261909"
    CLICK_IMAGE = str(
        get_project_root() / "resources" / "data_test" / "file_upload"
        / "quy_hoach_su_dung_dat" / "tra_cuu" / "QHSDD_TRA_CUU_NO_LOGIN_007"
        / "QHSDD_TRA_CUU_NO_LOGIN_007.png"
    )
    TEST_NAME = "QHSDD_TRA_CUU_LOGIN_008"

    def test_click_nut_x_dong_popup(self, map_page: MapPage, yolo_engine, screenshot_dir):
        thresh_hold = get_thresh_hold(self.TEST_NAME)
        mp = map_page

        mp.click_quy_hoach_su_dung_dat_tab()
        mp.click_search_box()
        mp.search_with_retry(self.DIA_CHI)
        mp.click_first_result()

        # Đóng popup
        mp.close_popup_dieu_huong()
        mp.wait_not_visible(mp.POPUP_DIA_CHI_CHI_TIET, timeout=5000)

        wait_for_map_stable(mp.page, screenshot_dir, yolo_engine)

        # Click trên bản đồ
        screenshot_path = take_screenshot(mp.page, screenshot_dir)
        click_result = yolo_engine.find_small_image_in_large(
            screenshot_path, self.CLICK_IMAGE,
            min_template_threshold=thresh_hold[0] if thresh_hold else 0.1,
        )
        assert len(click_result) >= 1, "⚠️ Không tìm thấy vị trí click"
        x, y = click_result[0]
        mp.click_on_map(x, y)
        time.sleep(1)

        # Verify cảnh báo không có dữ liệu
        mp.wait_visible(mp.POPUP_CANH_BAO_CHUA_CO_DU_LIEU_QHSD_DAT, timeout=mp.wait_timeout)
