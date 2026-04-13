# multi-backend-rest-api-demo

此專案由 `Laravel + Flask + Django Demo` Fork 而來，目標不是一次性展示，而是作為後續持續擴充的多後端 REST API 對照專案。

## 專案定位

- 以同一個業務主題（Task API）對照三種後端框架的實作方式。
- 保留各框架原生結構，避免過度抽象，方便學習與比較。
- 後續會逐步補齊一致的 API 規格、測試與文件。

## 目前目錄

```text
multi-backend-rest-api-demo/
├─ laravel-app/
├─ flask-app/
├─ django-app/
├─ requirements.txt
└─ README.md
```

## 目前各後端狀態

### Laravel

- 路由檔：`laravel-app/routes/web.php`
- 目前頁面：
  - `/` -> `hello` 視圖
  - `/welcome` -> `welcome` 視圖

啟動：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\laravel-app
php artisan serve --port=8001
```

### Flask

- 進入點：`flask-app/app.py`
- 目前頁面：
  - `/` -> `templates/index.html`

啟動：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\flask-app
python -m venv .venv
.\.venv\Scripts\activate
pip install flask
python app.py
```

### Django

- 路由檔：`django-app/config/urls.py`
- 檢視檔：`django-app/config/views.py`
- 目前頁面：
  - `/` -> `templates/index.html`

啟動：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo\django-app
python -m venv .venv
.\.venv\Scripts\activate
pip install django
python manage.py runserver 8002
```

## Python 共同套件

根目錄 `requirements.txt` 目前包含：

```txt
flask
django
```

安裝方式：

```powershell
cd F:\xampp\htdocs\multi-backend-rest-api-demo
pip install -r requirements.txt
```

## 開發約定（建議）

- **埠號規劃**
  - Laravel：`8001`
  - Flask：`5000`
  - Django：`8002`
- **一致性目標**
  - 相同資源命名（例如 `/api/tasks`）
  - 相同回應格式（欄位名稱、錯誤格式）
  - 相同測試情境（CRUD、驗證、錯誤處理）

## 後續 Roadmap

- 建立三端一致的 Task REST API（CRUD）。
- 補齊 Postman 或 OpenAPI 規格檔。
- 加上最小可用測試（Laravel/PHPUnit、Flask/Pytest、Django/TestCase）。
- 規劃資料庫策略（先 SQLite，再視需求切換 MySQL/MariaDB）。

## 備註

- 目前專案仍保留 Demo 性質內容，會分階段轉為可長期維護的 API 對照範本。
- 若要新增規範（程式風格、commit 規則、API 設計原則），建議直接更新本 README 作為單一準則入口。
# multi-backend-rest-api-demo

A unified RESTful Task API implemented with Laravel, Flask, and Django to compare backend architectures and design patterns.



\# Laravel + Flask + Django Demo



此專案目標：快速建立三個環境，並各自輸出 `Hello world`。



> 該專案為工作測試內容使用 XAMPP \& Anaconda \& Windows，正式開發建議使用 Ubuntu、OpenSuSE、Docker、MariaDB。



\## 1) Laravel (PHP)



\### 建立專案



```powershell

cd f:\\xampp\\htdocs\\laravel-flask-django-demo

composer create-project laravel/laravel laravel-app

```



> 若下載過程超時，可先設定：

>

> ```powershell

> $env:COMPOSER\_PROCESS\_TIMEOUT=1800

> composer create-project laravel/laravel laravel-app

> ```



\### 下載過慢時（Laravel/Composer）



XAMPP，請先打開：



`F:\\xampp\\php\\php.ini`



找到這行（可用 Ctrl+F 搜尋）：



```ini

;extension=zip

```



把前面的 `;` 拿掉，改成：



```ini

extension=zip

```



完成後請重新開啟終端機，再重新執行：



```powershell

composer create-project laravel/laravel laravel-app

```



\### 修改路由為 Hello world



編輯 `laravel-app\\routes\\web.php`：



```php

<?php



use Illuminate\\Support\\Facades\\Route;



Route::get('/', function () {

&#x20;   return view('hello');

});



Route::get('/welcome', function () {

&#x20;   return view('welcome');

});

```



註記：`hello.blade.php` 是由原本的 `welcome.blade.php` 複製後，再依需求改成自己的內容（例如加上 Hello World 與測試紀錄）。



\### 啟動



```powershell

cd laravel-app

php artisan serve

```



開啟：`http://127.0.0.1:8000`



若要改埠號：



```powershell

php artisan serve --port=8001

```



開啟：`http://127.0.0.1:8001`



\---



\## 2) Flask (Python)



\### 建立專案與虛擬環境



```powershell

cd f:\\xampp\\htdocs\\laravel-flask-django-demo

mkdir flask-app

cd flask-app

python -m venv .venv

.\\.venv\\Scripts\\activate

pip install flask

```



\### 建立 `app.py`



```python

from flask import Flask



app = Flask(\_\_name\_\_)



@app.route("/")

def hello():

&#x20;   return "Hello world from Flask!"



if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   app.run(debug=True, port=5000)

```



\### 啟動



```powershell

cd f:\\xampp\\htdocs\\laravel-flask-django-demo\\flask-app

.\\.venv\\Scripts\\activate

python app.py

```



開啟：`http://127.0.0.1:5000`



若要改埠號（擇一）：



```powershell

flask run --port 5001

```



或修改 `app.py`：



```python

if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   app.run(debug=True, port=5001)

```



開啟：`http://127.0.0.1:5001`



\---



\## 3) Django (Python)



\### 建立專案與虛擬環境



```powershell

cd f:\\xampp\\htdocs\\laravel-flask-django-demo

mkdir django-app

cd django-app

python -m venv .venv

.\\.venv\\Scripts\\activate

pip install django

django-admin startproject config .

```



\### 設定 Hello world 路由



編輯 `django-app\\config\\views.py`：



```python

from django.http import HttpResponse



def hello(request):

&#x20;   return HttpResponse("Hello world from Django!")

```



編輯 `django-app\\config\\urls.py`：



```python

from django.contrib import admin

from django.urls import path

from .views import hello



urlpatterns = \[

&#x20;   path("admin/", admin.site.urls),

&#x20;   path("", hello),

]

```



\### 啟動



```powershell

cd f:\\xampp\\htdocs\\laravel-flask-django-demo\\django-app

.\\.venv\\Scripts\\activate

python manage.py runserver

```



開啟：`http://127.0.0.1:8000`



若要改埠號：



```powershell

python manage.py runserver 8002

```



開啟：`http://127.0.0.1:8002`



\---



\## Python 套件安裝（requirements.txt）



專案根目錄提供 `requirements.txt`，目前包含：



```txt

flask

django

```



使用方式：



```powershell

cd f:\\xampp\\htdocs\\laravel-flask-django-demo

pip install -r requirements.txt

```



\## 建議目錄結構



```text

laravel-flask-django-demo/

&#x20; ├─ laravel-app/

&#x20; ├─ flask-app/

&#x20; ├─ django-app/

&#x20; ├─ requirements.txt

&#x20; └─ README.md

```



\## 備註



\- Laravel 與 Django 預設都可能使用 `8000` 連接埠，請避免同時啟動或改埠號。

\- 改埠號範例：

&#x20; - Laravel：`php artisan serve --port=8001`

&#x20; - Flask：`flask run --port 5001`（或 `app.run(port=5001)`）

&#x20; - Django：`python manage.py runserver 8002`



