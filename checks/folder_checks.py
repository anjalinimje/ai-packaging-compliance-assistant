import os
import re

def validate_naming_standard(package_path):

    if not os.path.exists(package_path):
        return None

    version = os.path.basename(package_path)

    if not re.match(r"^\d+(\.\d+)*$", version):
        return {
            "valid": False,
            "remark": f"Invalid version folder: {version}"
        }

    application = os.path.basename(
        os.path.dirname(package_path)
    )

    vendor = os.path.basename(
        os.path.dirname(
            os.path.dirname(package_path)
        )
    )

    found_path = f"{vendor}\\{application}\\{version}"

    invalid_names = [
        "",
        "downloads",
        "desktop",
        "documents",
        "users",
        "applications",
        "source",
        "global",
        "canada",
        "uson"
    ]

    if vendor.lower() in invalid_names:

        return {
            "valid": False,
            "remark":
            f"Naming standard not followed. Found: {found_path}. Expected: Vendor\\Application\\Version"
        }

    if re.match(r"^\d+(\.\d+)*$", application):

        return {
            "valid": False,
            "remark":
            f"Application folder missing. Found: {found_path}"
        }

    return {
        "valid": True,
        "vendor": vendor,
        "application": application,
        "version": version
    }