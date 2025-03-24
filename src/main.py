"""
Handles user interactions, controls the installer flow and triggers the appropriate functions
"""
from parser import parse_command
from installer import install_software
from utils import get_os


def main():
    user_prompt = input("What software would you like to install?")
    parsed_command = parse_command(user_prompt)

    action = parsed_command["action"]

    if action == "install":
        for software in parsed_command["software_name"]:
            install_software(software)
    else:
        print(f"Action '{parse_command['action']}' not supported")

if __name__ == "__main__":
    main()