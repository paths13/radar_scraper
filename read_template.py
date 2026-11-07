with open(
    "email_template.txt",
    "r",
    encoding="utf-8-sig"
) as file:
    email_text = file.read()
    company = 'ООО "ФИДЕСИС"'
    email_text = email_text.replace(
    "{company}",
    company
)
    print(email_text)
