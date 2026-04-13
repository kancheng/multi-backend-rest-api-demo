# multi-backend-rest-api-demo

此專案由 `Laravel + Flask + Django Demo` Fork 而來，現階段定位為「同一份需求，在三種後端框架中平行實作」的長期維護專案。

## 專案目標

- 建立可對照的 Laravel / Flask / Django REST API 實作。
- 維持三端功能一致，方便比較設計、效能與開發流程。
- 作為後續擴充（驗證、測試、文件、自動化）的基礎。

## 專案結構

```text
multi-backend-rest-api-demo/
├─ laravel-app/
├─ flask-app/
├─ django-app/
├─ requirements.txt
└─ README.md
```

## 目前狀態

### Laravel

- 應用目錄：`laravel-app`
- 路由：`laravel-app/routes/web.php`
- 已實作 Smart Pantry REST API（`/api/ingredients` 等）
- 現有頁面：
  - `/` -> `pantry` view（食材列表、新增／編輯／刪除／使用紀錄，透過 `fetch` 呼叫同一套 API）
  - `/welcome` -> `welcome` view
- 若曾出現 **Blade 中文變 `?`** 或 Django **`UnicodeDecodeError`（例如 `0xb7`）**：代表範本不是有效 UTF-8（常見於標題裡的 `·` 變成單一位元組）。請勿手動貼上破壞編碼的內容；可從 Flask 範本重新產生：
  - Laravel：`python laravel-app/scripts/build_pantry_view.py`
  - Django：`python django-app/scripts/build_index_template.py`

啟動（建議埠號 `8001`）：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\laravel-app
php artisan migrate
php artisan serve --port=8001
```

### Flask

- 應用目錄：`flask-app`
- 進入點：`flask-app/app.py`
- 已實作 Smart Pantry REST API（`/api/ingredients` 等，MySQL）
- 現有頁面：
  - `/` -> `flask-app/templates/index.html`（食材 CRUD 網頁介面）

啟動（建議埠號 `5000`）：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\flask-app
python -m venv .venv
.\.venv\Scripts\activate
pip install flask
python app.py
```

### Django

- 應用目錄：`django-app`
- 路由：`django-app/config/urls.py`
- 視圖：`django-app/config/views.py`
- 已實作 Smart Pantry REST API（`/api/ingredients` 等）
- 現有頁面：
  - `/` -> `django-app/templates/index.html`（食材 CRUD 網頁介面）

啟動（建議埠號 `8002`）：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\django-app
python -m venv .venv
.\.venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver 8002
```

## Smart Pantry API 一覽（三端一致）

- `GET /api/ingredients`
- `GET /api/ingredients/{id}`
- `POST /api/ingredients`
- `PUT /api/ingredients/{id}`
- `DELETE /api/ingredients/{id}`
- `POST /api/ingredients/{id}/use`
- `GET /api/ingredients/{id}/usage`
- `GET /api/ingredients/expiring`
- `GET /api/ingredients/low-stock`

## Python 套件（共用）

`requirements.txt` 目前包含：

```txt
flask
django>=4.2,<5
pymysql
mysqlclient>=2.2.1
python-dotenv
```

Django 連 MySQL 需使用 **mysqlclient**（2.2.1+）。請勿在 `config/__init__.py` 使用 `pymysql.install_as_MySQLdb()`，否則版本檢查會失敗。Flask 仍直接使用 `pymysql`。

為相容常見 XAMPP 內建的 **MariaDB 10.4**，`requirements.txt` 將 Django 限制在 **4.2 LTS**（`django>=4.2,<5`）。若你已升級 MariaDB **10.6+**，可自行改為安裝 Django 5。

安裝方式：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo
pip install -r requirements.txt
```

## 開發規範（本專案）

- 三個後端以「相同資源與相同語意」為原則（例如 `tasks`）。
- API 路徑、回應欄位、錯誤格式盡量一致。
- 變更功能時，優先同步更新三端與 README。
- 預設埠號：
  - Laravel：`8001`
  - Flask：`5000`
  - Django：`8002`

## 下一步計畫

1. 定義第一版統一 API 規格（建議：`/api/tasks` CRUD）。
2. 補齊三端對應實作與最小測試。
3. 補上 API 文件（Postman collection 或 OpenAPI）。
4. 加入一致的錯誤格式與驗證規則。

## 說明

這份 README 以「目前狀態 + 開發方向」為主，不再記錄從零建立框架的流程。若需初始化教學，請另建 `docs/setup-from-scratch.md` 以維持主文件精簡。

## 改用 XAMPP MySQL（Laravel / Flask / Django）


1. 先啟動 XAMPP 的 `Apache` 與 `MySQL`。
2. 在 phpMyAdmin 匯入 `setup_mysql.sql`（或用 MySQL CLI 執行）。
3. 三端連線設定已預設完成：
   - `laravel-app/.env`
   - `flask-app/.env`
   - `django-app/.env`
4. 執行 migration / seed：
   - Laravel：`php artisan migrate --seed`
   - Django：`python manage.py migrate`
   - Flask：啟動 `python app.py` 會自動建表與初始資料
