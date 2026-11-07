
import csv
import os
my_name = "Ольга Мараева"
my_email = "your_email@example.com"

# Читаем HTML-шаблон
with open(
    "email_template.html",
    "r",
    encoding="utf-8"
) as file:
    template = file.read()

os.makedirs("prepared_emails", exist_ok=True)

# Читаем список контактов
with open(
    "contacts.csv",
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:

    reader = csv.DictReader(file)

    for number, contact in enumerate(reader, start=1):

        company = contact.get("company")
        recipient = contact.get("email")

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

        output_file = f"prepared_emails/email_{number:03d}.html"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:
           file.write(email_html)

        print("Письмо сохранено:", output_file) 
