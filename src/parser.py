# parser.py (NLP Logic)
import spacy
import subprocess
from utils import get_os, is_software_installed

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def parse_command(user_prompt):
    """
    Extracts action (install, update, uninstall) and software names.
    """
    doc = nlp(user_prompt.lower())

    # Identify action keywords
    action = None
    if "install" in user_prompt.lower():
        action = "install"
    elif "uninstall" in user_prompt.lower() or "remove" in user_prompt.lower():
        action = "uninstall"
    elif "update" in user_prompt.lower():
        action = "update"

    # Extract potential software names (using noun phrases)
    software_names = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    return {
        "action": action,
        "software": software_names
    }

def install_software(software_name):
    os_type = get_os()

    # Check if software is already installed
    if is_software_installed(software_name):
        print(f"✅ {software_name} is already installed.")
        return

    # Default to automatic package manager search for minimal intervention
    command = {
        "windows": f"winget install {software_name} --silent --accept-package-agreements --accept-source-agreements",
        "mac": f"brew install {software_name}",
        "linux": f"sudo apt install {software_name} -y"
    }.get(os_type)

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {software_name} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing {software_name}: {e}")

def uninstall_software(software_name):
    os_type = get_os()

    uninstall_commands = {
        "windows": f"winget uninstall {software_name} --silent",
        "mac": f"brew uninstall {software_name}",
        "linux": f"sudo apt remove {software_name} -y"
    }

    if is_software_installed(software_name):
        try:
            command = uninstall_commands.get(os_type)
            subprocess.run(command, shell=True, check=True)
            print(f"✅ {software_name} uninstalled successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error uninstalling {software_name}: {e}")
    else:
        print(f"⚠️ {software_name} is not currently installed.")
