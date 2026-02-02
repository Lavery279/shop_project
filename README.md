# Shop Cosiness

Простий інтернет-магазин на Django з Vite + Tailwind для фронтенду.

---

## Опис
Проєкт реалізує каталог товарів, категорії, відгуки, кошик і оформлення замовлень.
## Примітка
У репозиторії збережені згенеровані стилі (`dist/`) та приклади картинок (`media/`),
щоб можна було одразу запустити проєкт і подивитися результат без додаткових кроків.

## Функціональність
- Реєстрація та кастомна модель користувача (`CustomUser`)
- Категорії та товари (`Category`, `Product`)
- Відгуки та рейтинг товарів (`Review`)
- Оформлення замовлень, позиції замовлення та статуси (`Order`, `OrderItem`, `OrderStatus`)
- Завантаження зображень для товарів

## Технології
- Backend: **Django 6.0**
- Frontend: **Vite**, **Tailwind CSS**
- База даних: SQLite (за замовчуванням)
- Важливі пакети: `django-tailwind`, `django-unfold`, `pillow`, `python-dotenv`, `shortuuid`

## Структура проєкту
```
shop/
├── catalog/               # Основний Django-додаток
│   ├── fixtures/          # JSON-фікстури для товарів, категорій, статусів
│   ├── migrations/        # Міграції бази даних
│   ├── static/catalog/    # Статичні файли (CSS, JS, зображення)
│   │   └── dist/          # Згенеровані Vite-стилі та скрипти
│   ├── templates/catalog/ # HTML-шаблони сторінок (index, cart, profile тощо)
│   ├── views/             # Логіка представлень (views, forms, urls)
│   └── models.py, forms.py, urls.py, etc.
├── config/                # Налаштування Django (settings, urls, wsgi)
├── media/                 # Завантажені зображення товарів
├── scripts/               # Скрипти для фікстур (наприклад, load_fixtures_and_fix_products.py)
├── templates/errors/      # Кастомні шаблони помилок
├── .env                   # Конфігурація середовища
├── .gitignore             # Ігноровані файли
├── manage.py              # Django-менеджер
└── requirements.txt       # Залежності Python
```

## Швидкий старт (локально)
1. Клонувати репозиторій і перейти в папку `shop`:

```bash
git clone <repo-url>
cd project_shop/shop
```

2. Створити та активувати віртуальне середовище (Windows):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Встановити залежності:

```bash
pip install -r requirements.txt
```

4. Створити файл `.env` поруч з `manage.py` з мінімальними змінними:

```env
SECRET_KEY=your_secret_key_here
IS_PRODUCTION=false
ALLOWED_HOSTS=localhost,127.0.0.1
```


5. Застосувати міграції та підвантажити фікстури (рекомендується через скрипт):

```bash
python manage.py migrate
python manage.py createsuperuser   # опційно, якщо потрібен суперкористувач
python scripts/load_fixtures_and_fix_products.py
```

> Скрипт робить:
> - Завантажує `categories.json` у базу.
> - Робить бекап `products.json` → `products.json.bak` і підставляє у `products.json` реальні ID категорій (пошук по `name`).
> - Завантажує оновлений `products.json`.
> - Завантажує `order_statuses.json`.

6. Запустити Django-сервер:

```bash
python manage.py runserver
```


## Деплой
- Статичні файли збираються командою:
  ```bash
  python manage.py collectstatic
  ```
- Медіа завантажуються вручну або через адмінку.


