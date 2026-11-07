import csv


INPUT_FILE = "radar_companies.csv"
OUTPUT_FILE = "contacts.csv"


def main():

    contacts = []

    seen_emails = set()

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            company = row.get(
                "name",
                ""
            ).strip()

            email = row.get(
                "email",
                ""
            ).strip().lower()

            if not email:
                continue

            if email in seen_emails:
                continue

            seen_emails.add(email)

            contacts.append({
                "company": company,
                "email": email,
                "status": "not_sent"
            })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        fieldnames = [
            "company",
            "email",
            "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(contacts)

    print()
    print("=" * 50)
    print("CONTACT LIST CREATED")
    print("=" * 50)

    print()
    print(
        "Unique contacts:",
        len(contacts)
    )

    print()
    print(
        f"File saved as: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
