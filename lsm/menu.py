"""
Interactive CLI menu module
"""

# Imports
import os  # Os module for the 'clear' command.
import sys  # Sys module for the 'exit' command.
import config  # Config module for the setter functions.
import cron  # Cron module for the crontab manipulations.


# Menu decorator
def menu_decorator(menu):
    def wrapper():
        os.system("clear")
        print "Light System Monitor\n"
        menu()
        print
        if menu.__name__[:3] == "sub":
            print "9. Back"
        if menu.__name__ == "menu_main":
            print "0. Exit"
        else:
            print "0. Main menu"
        choice = raw_input(">>  ")
        exec_menu(choice, menu.__name__)

    return wrapper


# Main menu1
@menu_decorator
def menu_main():
    print "Please choose an option:"
    print "1. Crontab configuration"
    print "2. Alerts configuration"
    print "3. Email configuration"


# Execute menu
def exec_menu(choice, current_menu):
    try:
        menu_actions[current_menu][choice]()
    except KeyError:
        menu_actions[current_menu][current_menu]()


# Exit program
def app_exit():
    os.system("clear")
    sys.exit(0)


# Crontab menu
@menu_decorator
def menu_cron():
    print "Crontab configuration\n"
    if cron.is_set():
        print "Crontab is set\n"
    print "1. Add to crontab"
    print "2. Remove from crontab"


# Add to crontab
def menu_cron_add():
    cron.add()
    exec_menu("menu_cron", "menu_cron")


# Remove from crontab
def menu_cron_remove():
    cron.remove()
    exec_menu("menu_cron", "menu_cron")


# Alerts menu
@menu_decorator
def menu_alerts():
    print "Alerts configuration\n"
    print "1. Processes"
    print "2. Thresholds"


# Alerts - Processes sub-menu
@menu_decorator
def submenu_alerts_processes():
    print "Alerts configuration -> Processes\n"
    print "Watched processes: {}\n".format(", ".join(config.list_processes()))
    print "1. Add process"
    print "2. Remove process"


# Alerts - Processes - Add
@menu_decorator
def submenu_alerts_processes_add():
    print "Alerts configuration -> Processes -> Add Process\n"
    process = raw_input("Please enter a process to watch: ")
    if config.add_process(process):
        print "{} added to the watch list!".format(process)
    else:
        print "Failed to add!"
    raw_input("Press enter to acknowledge.")
    # TODO - Maybe there's no need for this output and it's easier to see the results in the parent menu.
    exec_menu("submenu_alerts_processes", "submenu_alerts_processes")


# Alerts - Processes - Remove
@menu_decorator
def submenu_alerts_processes_remove():
    print "Alerts configuration -> Processes -> Remove Process\n"
    process = raw_input("Please enter a process to remove from watching: ")
    if config.remove_process(process):
        print "{} removed from the watch list!".format(process)
    else:
        print "Failed to remove!"
    raw_input("Press enter to acknowledge.")
    # TODO - Maybe there's no need for this output and it's easier to see the results in the parent menu.
    exec_menu("submenu_alerts_processes", "submenu_alerts_processes")


# Alerts - Thresholds sub-menu
@menu_decorator
def submenu_alerts_thresholds():
    print "Alerts configuration -> Thresholds\n"
    print "1. Set CPU percentage threshold"
    print "2. Set Memory percentage threshold"
    print "3. Set Swap memory percentage threshold"
    print "4. Set Core Temperature threshold"


# Alerts - Thresholds sub-menu - Set CPU
@menu_decorator
def submenu_alerts_thresholds_cpu():
    print "Alerts configuration -> Thresholds -> CPU percentage\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_cpu_percent(int(threshold))
    exec_menu("submenu_alerts_thresholds", "submenu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Set Memory
@menu_decorator
def submenu_alerts_thresholds_memory():
    print "Alerts configuration -> Thresholds -> Memory percentage\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_memory_percent(int(threshold))
    exec_menu("submenu_alerts_thresholds", "submenu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Set Swap
@menu_decorator
def submenu_alerts_thresholds_swap():
    print "Alerts configuration -> Thresholds -> Swap percentage\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_swap_percent(int(threshold))
    exec_menu("submenu_alerts_thresholds", "submenu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Core temperature
@menu_decorator
def submenu_alerts_thresholds_temp_core():
    print "Alerts configuration -> Thresholds -> Core temperature\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_temp_core(int(threshold))
    exec_menu("submenu_alerts_thresholds", "submenu_alerts_thresholds")


# Email menu
@menu_decorator
def menu_email():
    print "Email configuration\n"
    print "1. Recipient address"
    print "2. SMTP server"


# Email - Recipient sub-menus
@menu_decorator
def submenu_email_recipient():
    print "Email configuration -> Recipient address\n"
    print "Currently set address: {}\n".format(config.settings["email"]["address"])
    print "1. Change address"


# Email - Change the recipient
@menu_decorator
def submenu_email_recipient_change():
    print "Email configuration -> Recipient address -> Address change\n"
    address = raw_input("Please enter a new address: ")
    config.set_email(address)
    exec_menu("submenu_email_recipient", "submenu_email_recipient")


# Email - SMTP sub-menus
@menu_decorator
def submenu_email_smtp():
    print "Email configuration -> SMTP configuration\n"
    print "Currently set server: {}".format(config.settings["email"]["smtp_server"])
    print "Currently set username: {}".format(config.settings["email"]["smtp_user"])
    print "Currently set password: {}\n".format(config.settings["email"]["smtp_pass"])
    print "1. Change address"
    print "2. Change username"
    print "3. Change password"


# Email - Change the SMTP server
@menu_decorator
def submenu_email_smtp_change():
    print "Email configuration -> SMTP configuration -> Server change\n"
    server = raw_input("Please enter a new server domain name or IP: ")
    config.set_smtp(server)
    exec_menu("submenu_email_smtp", "submenu_email_smtp")


# Email - Change the SMTP username
@menu_decorator
def submenu_email_smtp_user():
    print "Email configuration -> SMTP configuration -> Username change\n"
    username = raw_input("Please enter a new SMTP username: ")
    config.set_smtp_user(username)
    exec_menu("submenu_email_smtp_user", "submenu_email_smtp_user")


# Email - Change the SMTP password
@menu_decorator
def submenu_email_smtp_pass():
    print "Email configuration -> SMTP configuration -> Password change\n"
    server = raw_input("Please enter a new SMTP password: ")
    config.set_smtp_pass(server)
    exec_menu("submenu_email_smtp_pass", "submenu_email_smtp_pass")


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
        "1": submenu_alerts_processes,
        "2": submenu_alerts_thresholds,
        "0": menu_main,
    },
    "submenu_alerts_processes": {
        "submenu_alerts_processes": submenu_alerts_processes,
        "1": submenu_alerts_processes_add,
        "2": submenu_alerts_processes_remove,
        "9": menu_alerts,
        "0": menu_main,
    },
    "submenu_alerts_thresholds": {
        "submenu_alerts_thresholds": submenu_alerts_thresholds,
        "1": submenu_alerts_thresholds_cpu,
        "2": submenu_alerts_thresholds_memory,
        "3": submenu_alerts_thresholds_swap,
        "4": submenu_alerts_thresholds_temp_core,
        "9": menu_alerts,
        "0": menu_main,
    },
    "menu_email": {
        "menu_email": menu_email,
        "1": submenu_email_recipient,
        "2": submenu_email_smtp,
        "0": menu_main,
    },
    "submenu_email_recipient": {
        "submenu_email_recipient": submenu_email_recipient,
        "1": submenu_email_recipient_change,
        "9": menu_email,
        "0": menu_main,
    },
    "submenu_email_smtp": {
        "submenu_email_smtp": submenu_email_smtp,
        "1": submenu_email_smtp_change,
        "2": submenu_email_smtp_user,
        "3": submenu_email_smtp_pass,
        "9": menu_email,
        "0": menu_main,
    }
}
