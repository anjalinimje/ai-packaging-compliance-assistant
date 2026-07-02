import os
from datetime import datetime

from sympy import content

MAX_DAYS = 15


def check_logs(documents_path):

    logs_path = os.path.join(documents_path, "Logs")

    if not os.path.isdir(logs_path):
        return False, "Logs folder missing"

    log_files = []

    for f in os.listdir(logs_path):

        if f.lower().endswith(".log"):
            log_files.append(
                os.path.join(logs_path, f)
            )

    if not log_files:
        return False, "No log files found"

    latest = max(
        log_files,
        key=os.path.getmtime
    )

    modified = datetime.fromtimestamp(
        os.path.getmtime(latest)
    )

    age = (datetime.now() - modified).days

    return age <= MAX_DAYS, f"Latest log age: {age} days"


def check_qa_checklist(documents_path):

    for file in os.listdir(documents_path):

        name = file.lower()

        if "qa" in name and "checklist" in name:

            full_path = os.path.join(
                documents_path,
                file
            )

            modified = datetime.fromtimestamp(
                os.path.getmtime(full_path)
            )

            age = (
                datetime.now() - modified
            ).days

            return age <= MAX_DAYS, file

    return False, "QA Checklist not found"


def validate_readme(
    documents_path,
    vendor,
    application,
    version
):

    readme = os.path.join(
        documents_path,
        "Readme.txt"
    )

    if not os.path.exists(readme):
        return False, "Readme missing"

    with open(
        readme,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        content = f.read().lower()

    checks = [
        vendor.lower(),
        application.lower(),
        version.lower()
    ]

    missing = []

    if vendor.lower() not in content:
        missing.append(f"Vendor Name ({vendor})")

    if application.lower() not in content:
        missing.append(f"Application Name ({application})")

    if version.lower() not in content:
        missing.append(f"Version ({version})")

    if missing:
        return (
            False,
            "Readme does not contain: "
            + ", ".join(missing)
        )

    return (
        True,
        f"Readme contains Vendor ({vendor}), Application ({application}) and Version ({version})"
    )