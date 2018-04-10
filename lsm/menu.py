"""
Interactive CLI menu module
"""

# Imports
import os  # Os module for the 'clear' command.
import sys  # Sys module for the 'exit' command.
import config  # Config module for the setter functions.
import cron  # Cron module for the crontab manipulations.


# TODO - Add decorators

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
    print "1. Processes"
    print "2. Thresholds"
    print "\n0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_alerts")


# Alerts - Processes sub-menu
def menu_alerts_processes():
    print "Light System Monitor\n"
    print "Alerts configuration -> Processes\n"
    print "Watched processes: {}\n".format(", ".join(config.list_processes()))
    print "1. Add process"
    print "2. Remove process"
    print "\n9. Back"
    print "0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_alerts_processes")


# Alerts - Processes sub-menu
def menu_alerts_processes_add():
    print "Light System Monitor\n"
    print "Alerts configuration -> Processes -> Add Process\n"
    process = raw_input("Please enter a process to watch: ")
    if config.add_process(process):
        print "{} added to the watch list!".format(process)
    else:
        print "Failed to add!"
    raw_input("Press enter to acknowledge.")
    # TODO - Maybe there's no need for this output and it's easier to see the results in the parent menu.
    exec_menu("menu_alerts_processes", "menu_alerts_processes")


# Alerts - Processes sub-menu
def menu_alerts_processes_remove():
    print "Light System Monitor\n"
    print "Alerts configuration -> Processes -> Remove Process\n"
    process = raw_input("Please enter a process to remove from watching: ")
    if config.remove_process(process):
        print "{} removed from the watch list!".format(process)
    else:
        print "Failed to remove!"
    raw_input("Press enter to acknowledge.")
    # TODO - Maybe there's no need for this output and it's easier to see the results in the parent menu.
    exec_menu("menu_alerts_processes", "menu_alerts_processes")


# Alerts - Thresholds sub-menu
def menu_alerts_thresholds():
    print "Light System Monitor\n"
    print "Alerts configuration -> Thresholds\n"
    print "1. Set CPU percentage threshold"
    print "2. Set Memory percentage threshold"
    print "3. Set Swap memory percentage threshold"
    print "4. Set Core Temperature threshold"
    print "\n9. Back"
    print "0. Main menu"
    choice = raw_input(">>  ")
    exec_menu(choice, "menu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Set CPU
def menu_alerts_thresholds_cpu():
    print "Light System Monitor\n"
    print "Alerts configuration -> Thresholds -> CPU percentage\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_cpu_percent(int(threshold))
    exec_menu("menu_alerts_thresholds", "menu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Set Memory
def menu_alerts_thresholds_memory():
    print "Light System Monitor\n"
    print "Alerts configuration -> Thresholds -> Memory percentage\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_memory_percent(int(threshold))
    exec_menu("menu_alerts_thresholds", "menu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Set Swap
def menu_alerts_thresholds_swap():
    print "Light System Monitor\n"
    print "Alerts configuration -> Thresholds -> Swap percentage\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_swap_percent(int(threshold))
    exec_menu("menu_alerts_thresholds", "menu_alerts_thresholds")


# Alerts - Thresholds sub-menu - Core temperature
def menu_alerts_thresholds_temp_core():
    print "Light System Monitor\n"
    print "Alerts configuration -> Thresholds -> Core temperature\n"
    threshold = raw_input("Please enter the new threshold: ")
    config.set_temp_core(int(threshold))
    exec_menu("menu_alerts_thresholds", "menu_alerts_thresholds")


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
        "1": menu_alerts_processes,
        "2": menu_alerts_thresholds,
        "0": menu_main,
    },
    "menu_alerts_processes": {
        "menu_alerts_processes": menu_alerts_processes,
        "1": menu_alerts_processes_add,
        "2": menu_alerts_processes_remove,
        "9": menu_alerts,
        "0": menu_main,
    },
    "menu_alerts_thresholds": {
        "menu_alerts_thresholds": menu_alerts_thresholds,
        "1": menu_alerts_thresholds_cpu,
        "2": menu_alerts_thresholds_memory,
        "3": menu_alerts_thresholds_swap,
        "4": menu_alerts_thresholds_temp_core,
        "9": menu_alerts,
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
