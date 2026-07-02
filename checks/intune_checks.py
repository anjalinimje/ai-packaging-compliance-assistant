import os

def check_intune(intune_path):

    if not os.path.exists(intune_path):
        return False, "Intune folder missing"

    for root, dirs, files in os.walk(intune_path):

        for file in files:

            if file.lower().endswith(".intunewin"):
                return True, file

    return False, "No .intunewin file found"