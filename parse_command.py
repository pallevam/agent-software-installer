import os
import platform
import subprocess
import json
import spacy

nlp = spacy.load("en_core_web_sm")

with open("commands.json", "r") as f:
    COMMANDS = json.load(f)



def get_os():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        raise RuntimeError("Unsupported OS: {system}")

def parse_command(user_prompt):
    """
    Extracts action (install, update, uninstall) and software names
    """
    doc = nlp(user_prompt.lower())
    
    # Identify action keywords
    action = None
    if "install" in user_prompt.lower():
        action = "install"
    elif "update" in user_prompt.lower():
        action = "update"
    elif "uninstall" in user_prompt.lower() or "remove" in user_prompt.lower():
        action = "uninstall"

    software_name = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    return {
        "action": action,
        "software_name": software_name
    }

def install_software(software_name):
    os_type = get_os()

    if software_name in COMMANDS[os_type]:
        command = COMMANDS[os_type][software_name]

        try:
            subprocess.run(command, shell=True, check=True)
            print(f"{software_name} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {software_name}")
    else:
        print(f"Installation command for {software_name} not found")

if __name__ == "__main__":
    user_prompt = input("What software would you like to install?")
    parsed_command = parse_command(user_prompt)

    action = parsed_command["action"]

    if action == "install":
        for software in parsed_command["software_name"]:
            install_software(software)
    else:
        print(f"Action '{parse_command['action']}' not supported")

