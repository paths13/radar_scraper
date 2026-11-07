
import csv
import os

my_name = os.getenv("MY_NAME", "Your Name")
my_email = os.getenv("GMAIL_ADDRESS", "your-email@example.com")

# Загружаем HTML-шаблон
with open(
    "email_template.html",
    "r",
    encoding="utf-8"
) as file:
    template = file.read()

# Создаём папку для писем
os.makedirs("prepared_emails", exist_ok=True)

# Счётчики
prepared = 0
skipped = 0

# Читаем контакты
with open(
    "contacts.csv",
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:

    reader = csv.DictReader(file)

    for number, contact in enumerate(reader, start=1):

        company = (contact.get("company") or "").strip()
        recipient = (contact.get("email") or "").strip()
        status = (contact.get("status") or "").strip().lower()

        # Пропускаем уже отправленные письма
        if status == "sent":
            print(f"Пропуск: {company} — уже отправлено")
            skipped += 1
            continue

        # Проверяем наличие компании и email
        if not company or not recipient:
            print(f"Пропуск строки {number}: нет компании или email")
            skipped += 1
            continue

        # Персонализируем HTML
        email_html = template.replace(
            "{{ company }}",
            company
        )

        email_html = email_html.replace(
            "{{ name }}",
            my_name
        )

        email_html = email_html.replace(
            "{{ email }}",
            my_email
        )

        # Создаём имя файла
        output_file = (
            f"prepared_emails/email_{number:03d}.html"
        )

        # Сохраняем письмо
        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as output:

            output.write(email_html)

        print(f"Подготовлено: {company} -> {recipient}")

        prepared += 1

print()
print("Результат:")
print(f"Подготовлено писем: {prepared}")
print(f"Пропущено контактов: {skipped}")

