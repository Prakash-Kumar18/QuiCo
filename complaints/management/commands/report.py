from django.core.management.base import BaseCommand
from complaints.models import Complaint
from complaints.utils import build_stats, parse_enroll, short


class Command(BaseCommand):
    help = "Interactive complaint report"

    def handle(self, *args, **options):
        while True:                                         # while loop
            print("\n1. Summary\n2. Search by category\n3. Complaints by joining year\n4. Quit")
            choice = input("Enter choice: ").strip()        # input
            if choice == "":
                continue
            if choice not in ("1", "2", "3", "4"):
                print("Invalid choice, try again.")
                continue
            if choice == "4":
                print("Bye!")
                break

            if choice == "1":
                data = build_stats(Complaint.objects.all())
                print("Total:", data["total"])
                for label, count in data["status_rows"]:
                    print(f"  {label.ljust(12)} {count}")
                for row in data["ranking"]:
                    print(f"  #{row['rank']} {row['name']} - {row['count']}")

            elif choice == "2":
                word = input("Category word (e.g. mess): ").strip().lower()
                limit = 5
                raw = input("How many to show (default 5): ").strip()
                try:
                    limit = int(raw)
                except ValueError:
                    pass                                    # pass: keep default
                found = Complaint.objects.filter(category__icontains=word)[:limit]
                for i, c in enumerate(found, start=1):      # enumerate
                    print(f"{i}. {c.code.ljust(11)} {short(c.title, 30).ljust(30)} {c.status}")
                if not found:
                    print("Nothing found.")

            elif choice == "3":
                by_year = {}
                for c in Complaint.objects.all():
                    info = parse_enroll(c.enroll)
                    if info is None:
                        continue
                    by_year[info["year"]] = by_year.get(info["year"], 0) + 1
                for year, count in sorted(by_year.items()):
                    print(f"  Batch {year}: {count}")