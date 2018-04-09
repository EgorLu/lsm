"""
Interactive CLI menu module
"""

# Imports
import os  # Os module for the 'clear' command.
import sys  # Sys module for the 'exit' command.
import config  # Config module for the setter functions.
import cron  # Cron module for the crontab manipulations.


# Main menu
def menu_main():
    os.system("clear")
    print "Light System Monitor\n"
    print "Please choose an option:"
    print "1. Crontab configuration"
    print "2. Alerts configuration"
    print "3. Email configuration"
    print "\n0. Exit"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_main")


# Execute menu
def exec_menu(choice, current_menu):
    os.system("clear")
    try:
        menu_actions[current_menu][choice]()
    except KeyError:
        menu_actions[current_menu][current_menu]()


# Exit program
def app_exit():
    sys.exit(0)


# Crontab menu
def menu_cron():
    print "Light System Monitor\n"
    print "Crontab configuration\n"
    if cron.is_set():
        print "Crontab is set\n"
    print "1. Add to crontab"
    print "2. Remove from crontab"
    print "\n0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_cron")


# Add to crontab
def menu_cron_add():
    cron.add()
    exec_menu("menu_cron", "menu_cron")


# Remove from crontab
def menu_cron_remove():
    cron.remove()
    exec_menu("menu_cron", "menu_cron")


# Alerts menu
def menu_alerts():
    print "Light System Monitor\n"
    print "Alerts configuration\n"
    print "1. WORK IN PROGRESS"
    print "2. UNDER CONSTRUCTION"
    print "\n0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_alerts")


# Email menu
def menu_email():
    print "Light System Monitor\n"
    print "Email configuration\n"
    print "1. Recipient address"
    print "2. SMTP server"
    print "\n0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_email")


# Email - Recipient sub-menus
def menu_email_recipient():
    print "Light System Monitor\n"
    print "Email configuration -> Recipient address\n"
    print "Currently set address: {}\n".format(config.settings["email"]["address"])
    print "1. Change address"
    print "\n9. Back"
    print "0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_email_recipient")


# Email - Change the recipient
def menu_email_recipient_change():
    print "Light System Monitor\n"
    print "Email configuration -> Recipient address -> Address change\n"
    address = raw_input("Please enter a new address: ")
    config.set_email(address)
    exec_menu("menu_email_recipient", "menu_email_recipient")


# Email - SMTP sub-menus
def menu_email_smtp():
    print "Light System Monitor\n"
    print "Email configuration -> SMTP configuration\n"
    print "Currently set server: {}".format(config.settings["email"]["smtp_server"])
    print "Currently set username: {}".format(config.settings["email"]["smtp_user"])
    print "Currently set password: {}\n".format(config.settings["email"]["smtp_pass"])
    print "1. Change address"
    print "2. Change username"
    print "3. Change password"
    print "\n9. Back"
    print "0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_email_smtp")


# Email - Change the SMTP server
def menu_email_smtp_change():
    print "Light System Monitor\n"
    print "Email configuration -> SMTP configuration -> Server change\n"
    server = raw_input("Please enter a new server domain name or IP: ")
    config.set_smtp(server)
    exec_menu("menu_email_smtp", "menu_email_smtp")


# Email - Change the SMTP username
def menu_email_smtp_user():
    print "Light System Monitor\n"
    print "Email configuration -> SMTP configuration -> Username change\n"
    username = raw_input("Please enter a new SMTP username: ")
    config.set_smtp_user(username)
    exec_menu("menu_email_smtp_user", "menu_email_smtp_user")


# Email - Change the SMTP password
def menu_email_smtp_pass():
    print "Light System Monitor\n"
    print "Email configuration -> SMTP configuration -> Password change\n"
    server = raw_input("Please enter a new SMTP password: ")
    config.set_smtp_pass(server)
    exec_menu("menu_email_smtp_pass", "menu_email_smtp_pass")


# Menu definition
menu_actions = {
    "menu_main": {
        "menu_main": menu_main,
        "1": menu_cron,
        "2": menu_alerts,
        "3": menu_email,
        "0": app_exit,
    },
    "menu_cron": {
        "menu_cron": menu_cron,
        "1": menu_cron_add,
        "2": menu_cron_remove,
        "0": menu_main,
    },
    "menu_alerts": {
        "menu_alerts": menu_alerts,
        "0": menu_main,
    },
    "menu_email": {
        "menu_email": menu_email,
        "1": menu_email_recipient,
        "2": menu_email_smtp,
        "0": menu_main,
    },
    "menu_email_recipient": {
        "menu_email_recipient": menu_email_recipient,
        "1": menu_email_recipient_change,
        "9": menu_email,
        "0": menu_main,
    },
    "menu_email_smtp": {
        "menu_email_smtp": menu_email_smtp,
        "1": menu_email_smtp_change,
        "2": menu_email_smtp_user,
        "3": menu_email_smtp_pass,
        "9": menu_email,
        "0": menu_main,
    }
}
