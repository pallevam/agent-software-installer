"""
Contains essential utility functions like get_os() etc for apltform detection and is_software_installed() to check if a software is already installed
"""
import platform
import psutil

def is_software_installed(software_name):
    for proc in psutil.process_iter(['name']):
        if software_name in proc.info['name']:
            return True
    return False


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