"""
Configuration module

Takes care of the alerts and the SMTP settings.
"""

import json  # JSON module in order to work with the stored configuration file.
import os  # OS module to be able to check whether a file exists.
import re  # Regex module for the regex checks on field updates.

# Check whether the config file exists.
# If it doesn't exist, create an empty file.
if not os.path.isfile("./config.json"):
    settings = {
        "alerts": {
            "processes": [],
            "cpu_percent": 0,
            "memory_percent": 0,
            "swap_percent": 0,
            "temp_core": 0
        },
        "email": {
            "address": "",
            "smtp_server": "",
            "smtp_user": "",
            "smtp_pass": ""
        }
    }
    json_settings = json.dumps(settings, indent=4, sort_keys=True)
    with open("./config.json", "w+") as f:
        f.write(json_settings)

# Open the config file.
with open("./config.json") as f:
    # Decode the JSON and load it's data.
    settings = json.loads(f.read())


def update():
    # TODO - Update only the relevant fields and not the entire document.
    json_settings = json.dumps(settings, indent=4, sort_keys=True)
    with open("./config.json", "w") as f:
        f.write(json_settings)


def set_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print "Email changed from {} to {}".format(settings["email"]["address"], email)
        settings["email"]["address"] = email
        update()


def set_smtp(smtp):
    if re.match(r"[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*", smtp):
        print "SMTP server changed from {} to {}".format(settings["email"]["smtp_server"], smtp)
        settings["email"]["smtp_server"] = smtp
        update()


def set_smtp_user(username):
    if re.match(r"[^\s]", username):
        print "SMTP username changed from {} to {}".format(settings["email"]["smtp_user"], username)
        settings["email"]["smtp_user"] = username
        update()


def set_smtp_pass(password):
    if re.match(r"[A-Za-z0-9@#$%^&*()\-_+=]", password):
        print "SMTP server changed from {} to {}".format(settings["email"]["smtp_pass"], password)
        settings["email"]["smtp_pass"] = password
        update()


def list_processes():
    return [process for process in settings["alerts"]["processes"]]


def add_process(process):
    if re.match(r"[a-zA-Z]+", process):
        process = process.lower()
        if process not in settings["alerts"]["processes"]:
            settings["alerts"]["processes"].append(process)
            update()
            return True
    return False


def remove_process(process):
    if re.match(r"[a-zA-Z]+", process):
        process = process.lower()
        if process in settings["alerts"]["processes"]:
            settings["alerts"]["processes"].remove(process)
            update()
            return True
    return False


def set_cpu_percent(value):
    """
    CPU percentage threshold setter.
    :param value: The percentage 0-100.
    :type value: int
    :return: None
    """
    if isinstance(value, int) and 0 <= value <= 100:
        settings["alerts"]["cpu_percent"] = value
        update()


def set_memory_percent(value):
    """
    RAM/DIMM percentage threshold setter.
    :param value: The percentage 0-100.
    :type value: int
    :return: None
    """
    if isinstance(value, int) and 0 <= value <= 100:
        settings["alerts"]["memory_percent"] = value
        update()


def set_swap_percent(value):
    """
    Swap memory percentage threshold setter.
    :param value: The percentage 0-100.
    :type value: int
    :return: None
    """
    if isinstance(value, int) and 0 <= value <= 100:
        settings["alerts"]["swap_percent"] = value
        update()


def set_temp_core(value):
    """
    Core Temperature percentage threshold setter.
    :param value: The percentage 0-100.
    :type value: int
    :return: None
    """
    if isinstance(value, int) and 0 <= value <= 100:
        settings["alerts"]["temp_core"] = value
        update()
