import re

def analyze_ps1(ps1_path):

    with open(
        ps1_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        content = f.read()

    results = {}

    results["hardcoded_c"] = bool(
        re.search(r"C:\\", content)
    )

    results["hardcoded_d"] = bool(
        re.search(r"D:\\", content)
    )

    results["silent_install"] = (
        "Execute-MSI" in content
        or "Execute-Process" in content
    )

    results["silent_uninstall"] = (
        "Remove-MSIApplications" in content
        or "Execute-MSI" in content
    )

    results["shortcut_logic"] = (
        ".lnk" in content
        or "Remove-Item" in content
    )

    install_pos = content.find(
        "Execute-Process"
    )

    uninstall_pos = content.find(
        "Remove-MSIApplications"
    )

    results["upgrade_logic"] = (
        uninstall_pos != -1
        and install_pos != -1
        and uninstall_pos < install_pos
    )

    return results