
import csv
from pathlib import Path
from email.message import EmailMessage
import os
import smtplib

from dotenv import load_dotenv
load_dotenv()

MY_EMAIL = os.getenv("GMAIL_ADDRESS")
MY_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not MY_EMAIL or not MY_PASSWORD:
    raise ValueError("Не найдены настройки Gmail в файле .env")


# Файл резюме
RESUME_PATH = Path("Мараева Ольга.pdf")

# Папка с подготовленными письмами
EMAILS_DIR = Path("prepared_emails")


def load_contacts():
    """Загружает контакты из CSV."""

    with open(
        "contacts.csv",
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        return list(csv.DictReader(file))

def load_sent_emails():
    """Загружает адреса, которым уже отправляли письма."""

    sent_emails = set()

    if not Path("sent_log.csv").exists():
        return sent_emails

    with open(
        "sent_log.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            email = row.get("email", "").strip().lower()

            if email:
                sent_emails.add(email)

    return sent_emails

from datetime import datetime


def save_sent_email(company, email):
    """Записывает успешную отправку в журнал."""

    with open(
        "sent_log.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            company,
            email,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])


def update_contact_status(email):
    """Обновляет статус контакта в contacts.csv."""

    contacts = load_contacts()

    for contact in contacts:

        if contact["email"].strip().lower() == email.strip().lower():
            contact["status"] = "sent"

    with open(
        "contacts.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = ["company", "email", "status"]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(contacts)

def create_email(contact, number):
    """Создаёт письмо для одной компании."""

    company = contact["company"].strip()
    recipient = contact["email"].strip()

    html_path = EMAILS_DIR / f"email_{number:03d}.html"

    if not html_path.exists():
        raise FileNotFoundError(
            f"HTML-файл не найден: {html_path}"
        )

    if not RESUME_PATH.exists():
        raise FileNotFoundError(
            f"Резюме не найдено: {RESUME_PATH}"
        )

    with open(
        html_path,
        "r",
        encoding="utf-8"
    ) as file:

        html_content = file.read()

    message = EmailMessage()

    message["From"] = MY_EMAIL
    message["To"] = recipient
    message["Subject"] = (
        f"Предложение о сотрудничестве — {company}"
    )

    message.set_content(
        "Здравствуйте! Направляю вам своё резюме."
    )

    message.add_alternative(
        html_content,
        subtype="html"
    )

    with open(RESUME_PATH, "rb") as file:
        resume_data = file.read()

    message.add_attachment(
        resume_data,
        maintype="application",
        subtype="pdf",
        filename="Olga_Maraeva_Resume.pdf"
    )

    return message

def send_email(message):
    """Отправляет одно письмо через Gmail."""

    print()
    print("=" * 50)
    print("ПОДТВЕРЖДЕНИЕ ОТПРАВКИ")
    print("=" * 50)

    print("Отправитель:", message["From"])
    print("Получатель:", message["To"])
    print("Тема:", message["Subject"])

    confirmation = input(
        "Для отправки именно этого письма введи YES: "
    ).strip()

    if confirmation != "YES":
        print("Отправка отменена.")
        return False

    try:
        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=30
        ) as server:

            server.starttls()

            server.login(
                MY_EMAIL,
                MY_PASSWORD
            )

            server.send_message(message)

        print("Письмо успешно отправлено!")
        return True

    except Exception as error:
        print("Не удалось отправить письмо.")
        print("Тип ошибки:", type(error).__name__)
        print("Описание:", error)
        return False


def main():

    contacts = load_contacts()
    sent_emails = load_sent_emails()

    for number, contact in enumerate(contacts, start=1):

        company = contact.get("company", "").strip()
        recipient = contact.get("email", "").strip()
        status = contact.get("status", "").strip().lower()

        # Пропускаем уже отправленные письма
        if status == "sent":
            continue

        # Пропускаем адреса из журнала
        if recipient.lower() in sent_emails:
            print(f"Пропуск: {recipient} уже есть в журнале.")
            continue

        # Проверяем данные контакта
        if not company or not recipient:
            print(f"Пропуск строки {number}: неполные данные.")
            continue

        # Создаём персональное письмо
        message = create_email(contact, number)

        # Отправляем только после подтверждения
        success = send_email(message)

        if success:

            # Записываем успешную отправку
            save_sent_email(company, recipient)

            # Обновляем статус контакта
            update_contact_status(recipient)

            print("Журнал и статус контакта обновлены.")

        else:
            print("Контакт не отмечен как отправленный.")

        # За один запуск обрабатываем только один контакт
        break


if __name__ == "__main__":
    main()
