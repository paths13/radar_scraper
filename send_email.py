import os
import smtplib

from pathlib import Path
from dotenv import load_dotenv
from email.message import EmailMessage


# Загружаем настройки из файла .env
load_dotenv()

# Получаем адрес Gmail и пароль приложения
gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_APP_PASSWORD")

# Проверяем, что настройки найдены
if not gmail_address or not gmail_password:
    raise ValueError("Не найдены настройки Gmail в файле .env")


def create_test_email():
    """Создаёт тестовое письмо и прикрепляет резюме."""

    message = EmailMessage()

    # Отправитель и получатель — собственный Gmail
    message["From"] = gmail_address
    message["To"] = gmail_address
    message["Subject"] = "Тестовое письмо — RADAR"

    # Текст письма
    message.set_content(
        "Здравствуйте! Это тестовое письмо из проекта RADAR."
    )

    # Находим файл резюме
    resume_path = Path("Мараева Ольга.pdf")

    if not resume_path.exists():
        raise FileNotFoundError(
            f"Файл резюме не найден: {resume_path}"
        )

    # Читаем PDF
    with open(resume_path, "rb") as file:
        resume_data = file.read()

    # Прикрепляем резюме
    message.add_attachment(
        resume_data,
        maintype="application",
        subtype="pdf",
        filename="Olga_Maraeva_Resume.pdf"
    )

    return message


def send_test_email():
    """Отправляет одно тестовое письмо на собственный Gmail."""

    message = create_test_email()

    print("Письмо подготовлено!")
    print(f"Отправитель: {gmail_address}")
    print(f"Получатель: {gmail_address}")
    print("Вложение: Olga_Maraeva_Resume.pdf")
    print()

    confirmation = input(
        "Для отправки введи YES: "
    ).strip()

    if confirmation != "YES":
        print("Отправка отменена. Письмо не отправлено.")
        return

    print("Подключаемся к Gmail...")

    try:
        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=30
        ) as server:

            server.starttls()

            server.login(
                gmail_address,
                gmail_password
            )

            server.send_message(message)

        print("Тестовое письмо успешно отправлено!")
        print("Проверь входящие и папку «Спам».")

    except Exception as error:
        print("Не удалось отправить письмо.")
        print(f"Тип ошибки: {type(error).__name__}")
        print(f"Описание: {error}")


if __name__ == "__main__":
    send_test_email()
