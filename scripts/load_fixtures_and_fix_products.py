import os
import django
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command
from catalog.models import Category
from django.contrib.auth import get_user_model

FIXTURES_DIR = BASE_DIR / "catalog" / "fixtures"
PRODUCTS_FILE = FIXTURES_DIR / "products.json"
BACKUP_FILE = FIXTURES_DIR / "products.json.bak"


def ensure_superuser(username="admin", email="admin@example.com", password="admin"):
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        print(f"Створюю суперкористувача: {username}")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Суперкористувач {username} вже існує.")


def load_initial():
    print("Запускаю міграції...")
    call_command("migrate", interactive=False)
    ensure_superuser()
    print("Завантажую categories fixture...")
    call_command("loaddata", str(FIXTURES_DIR / "categories.json"))


def fix_products_json():
    if not BACKUP_FILE.exists():
        PRODUCTS_FILE.replace(BACKUP_FILE)
        BACKUP_FILE.write_text(BACKUP_FILE.read_text())

    data = json.loads(BACKUP_FILE.read_text(encoding="utf-8"))

    cats = Category.objects.all()
    name_map = {c.name: str(c.id) for c in cats}
    print(f"Знайдено {len(cats)} категорій у БД.")

    changed = False
    for obj in data:
        model = obj.get("model", "")
        if model.endswith("product"):
            fields = obj.get("fields", {})
            cat_value = fields.get("category")
            if cat_value:
                new_id = None
                if cat_value in name_map:
                    new_id = name_map[cat_value]
                if new_id:
                    if fields["category"] != new_id:
                        fields["category"] = new_id
                        changed = True

    if changed:
        print("Оновлюю products.json з реальними ID категорій...")
        PRODUCTS_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        print("Зміни в products.json не потрібні.")


def load_remaining():
    print("Завантажую products fixture...")
    call_command("loaddata", str(FIXTURES_DIR / "products.json"))
    print("Завантажую order_statuses fixture...")
    call_command("loaddata", str(FIXTURES_DIR / "order_statuses.json"))


if __name__ == "__main__":
    load_initial()
    fix_products_json()
    load_remaining()
    print("Готово.")
