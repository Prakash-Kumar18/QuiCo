BRANCHES = {"CSE": "Computer Science", "BBA": "Business Admin", "ECE": "Electronics", "MEC": "Mechanical"}
VALID_URGENCY = ("Low", "Medium", "High")


# ---------- 1. String slicing + string methods ----------
def clean_name(raw):
    words = raw.strip().split()                       # strip, split
    return " ".join(w.capitalize() for w in words)    # capitalize, join


def capitalize_first(text):
    text = text.strip()
    return text[:1].upper() + text[1:]                # slicing


def short(text, limit=40):
    return text if len(text) <= limit else text[:limit - 3] + "..."


def parse_enroll(enroll):
    """E22CSE045 -> year 2022, branch CSE, roll 045"""
    enroll = enroll.strip().upper()
    if len(enroll) != 9 or not enroll.startswith("E"):
        return None
    year, code, roll = enroll[1:3], enroll[3:6], enroll[6:]   # slicing
    if not (year.isdigit() and code.isalpha() and roll.isdigit()):
        return None
    return {"year": "20" + year, "branch": BRANCHES.get(code, code), "roll": roll}


# ---------- 5. in / not in ----------
def validate_complaint(data, valid_categories):
    errors = []
    for field in ["name", "enroll", "title", "desc"]:
        if not data.get(field, "").strip():
            errors.append(f"{field.capitalize()} is required.")
    if errors:
        return errors
    if data.get("category") not in valid_categories:
        errors.append("Invalid category.")
    if data.get("urgency") not in VALID_URGENCY:
        errors.append("Invalid urgency.")
    if parse_enroll(data["enroll"]) is None:
        errors.append("Enrollment ID format should be like E22CSE045.")
    if len(data["desc"].strip()) < 10:
        errors.append("Details should be at least 10 characters.")
    if len(data["title"]) > 200:
        errors.append("Title is too long.")
    return errors


# ---------- 2,3,4,5,6. Loops, break/continue, enumerate, zip, dict, set ----------
def build_stats(complaints):
    category_count = {}                                # dictionary
    status_count = {"Pending": 0, "InProgress": 0, "Resolved": 0}
    blocks = set()                                     # set (unique values)
    total = 0

    for c in complaints:                               # for loop
        if c.status not in status_count:               # not in
            continue                                   # continue
        total += 1
        status_count[c.status] += 1
        category_count[c.category] = category_count.get(c.category, 0) + 1
        if c.block:
            blocks.add(c.block.strip().upper())

    ranked = sorted(category_count.items(), key=lambda item: item[1], reverse=True)
    ranking = [{"rank": i, "name": n, "count": cnt}
               for i, (n, cnt) in enumerate(ranked, start=1)]      # enumerate + list comprehension

    labels = ["Pending", "In Progress", "Resolved"]
    counts = [status_count["Pending"], status_count["InProgress"], status_count["Resolved"]]
    status_rows = list(zip(labels, counts))            # zip: two lists at once
    percent = round(counts[2] * 100 / total) if total else 0

    return {"total": total, "ranking": ranking, "status_rows": status_rows,
            "blocks": sorted(blocks), "resolved_percent": percent}


def first_urgent_pending(complaints):
    found = None
    for c in complaints:
        if c.status == "Resolved":
            continue
        if c.urgency == "High":
            found = c
            break                                      # break
    return found