import os

INSTALLER_EXTENSIONS = (
    ".exe",
    ".msi",
    ".msix",
    ".appx",
    ".appxbundle",
    ".msp"
)

def check_vendor_source(vendor_source):

    installers = []

    for file in os.listdir(vendor_source):

        if file.lower().endswith(
            INSTALLER_EXTENSIONS
        ):
            installers.append(file)

    return installers