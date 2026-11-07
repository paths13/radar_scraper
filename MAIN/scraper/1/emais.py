import csv
 
with open(
    "contacts.csv",
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:
 
    reader = csv.DictReader(file)
 
    for contact in reader:
        status = contact.get("status")
        if status == "not_sent":
            email = contact.get("email")
            print(email)
