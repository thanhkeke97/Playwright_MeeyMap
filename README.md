# Playwright Pure Python – Meeymaps Automation

Dự án chuyển đổi từ **Robot Framework + Browser Library** sang **Playwright thuần (Python + pytest)**.

## Cấu trúc dự án

```
playwright_tests/
├── conftest.py                # pytest fixtures (browser, auth, page objects)
├── pyproject.toml             # pytest config & markers
├── requirements.txt           # Python dependencies
│
├── config/
│   └── settings.py            # Load env config từ config/ui.yaml
│
├── core/
│   ├── auth_helper.py         # API login (MeeyID) → cookie injection
│   ├── screenshot_helper.py   # Chụp ảnh & chờ bản đồ ổn định
│   └── yolo_template_search.py # YOLO + Template matching (standalone)
│
├── pages/
│   ├── base_page.py           # Base page object (click, input, wait, ...)
│   ├── login_page.py          # Login popup page
│   └── map_page.py            # Map page – tất cả locator & hành động
│
└── tests/
    └── ui/
        └── quy_hoach_su_dung_dat/
            └── test_tra_cuu_qhsdd_login.py   # 8 test cases
```

## Cài đặt

```bash
cd playwright_tests
pip install -r requirements.txt
playwright install chromium
```

## Chạy tests

```bash
# Chạy tất cả test (mặc định env=stg)
pytest

# Chạy cụ thể 1 file
pytest tests/ui/quy_hoach_su_dung_dat/test_tra_cuu_qhsdd_login.py

# Chạy theo marker
pytest -m QHSDD

# Chọn môi trường khác
pytest --env dev

# Chạy headed (hiển thị trình duyệt)
pytest --headed

# Debug 1 test
pytest -k "test_qhsdd_tra_cuu_login_001" -s --headed
```

## Biến môi trường

Config được đọc từ `config/ui.yaml` (nằm trong project gốc). Biến `--env` mặc định `stg`.

| Biến | Mô tả |
|------|-------|
| `url` | URL ứng dụng (staging, dev, prod) |
| `username` / `password` | Credentials cho login API |
| `wait_timeout` | Timeout chờ element (ms) |
| `api_url` | URL API MeeyID |
| `browser_type` | Loại browser: chromium, firefox, webkit |

## Kiến trúc

### Fixtures (conftest.py)

| Scope | Fixture | Mô tả |
|-------|---------|-------|
| session | `env_config` | Load config từ YAML |
| session | `yolo_engine` | YOLO + template matching engine |
| session | `auth_tokens` | Login API → lấy token & cookies |
| function | `browser` | Khởi tạo browser |
| function | `context` | Browser context (video recording) |
| function | `page_with_cookie` | Page đã inject auth cookie |
| function | `map_page` | MapPage object sẵn sàng sử dụng |

### Page Object Model

- **BasePage**: Methods chung (`click_element`, `input_text`, `wait_visible`, `get_text`, ...)
- **MapPage**: Kế thừa BasePage, chứa tất cả locators và action methods cho trang bản đồ
- **LoginPage**: Actions đăng nhập qua UI

### Visual Testing (YOLO)

Sử dụng YOLO11 model + multi-scale template matching:
1. Chụp screenshot toàn trang
2. YOLO detect vùng chứa đối tượng
3. Template matching so khớp ảnh mẫu nhỏ trong vùng YOLO
4. Trả về tọa độ trung tâm của match tốt nhất

## Thêm test mới

1. Tạo file `test_*.py` trong thư mục `tests/ui/` tương ứng
2. Import `MapPage`, fixtures từ `conftest.py`
3. Đặt ảnh mẫu trong `resources/data_test/file_upload/`
4. Sử dụng `map_page` fixture làm entry point
5. Gọi `wait_for_map_stable()` sau mỗi thao tác di chuyển bản đồ

## So sánh với Robot Framework

| Robot Framework | Playwright Pure Python |
|-----------------|----------------------|
| `*** Test Cases ***` | `class Test*` / `def test_*` |
| `[Template]` keyword | Method gọi trực tiếp |
| `_SetupTC` variables | Class attributes |
| `MEEY GetLocator` | Locator constants |
| `MEEY Click` | `page.click()` / `click_element()` |
| Suite Setup/Teardown | `conftest.py` fixtures |
| `${EXECDIR}` | `get_project_root()` |
| `pabot` (parallel) | `pytest-xdist` |
