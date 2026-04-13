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
- 現有頁面：
  - `/` -> `hello` view
  - `/welcome` -> `welcome` view

啟動（建議埠號 `8001`）：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\laravel-app
php artisan serve --port=8001
```

### Flask

- 應用目錄：`flask-app`
- 進入點：`flask-app/app.py`
- 現有頁面：
  - `/` -> `flask-app/templates/index.html`

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
- 現有頁面：
  - `/` -> `django-app/templates/index.html`

啟動（建議埠號 `8002`）：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\django-app
python -m venv .venv
.\.venv\Scripts\activate
pip install django
python manage.py runserver 8002
```

## Python 套件（共用）

`requirements.txt` 目前包含：

```txt
flask
django
```

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
