#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
This file is responsible for scanning the system using the psutil,
checking the results against the initial alert configuration,
saving the scan report and updating the events log,
additionally, it generates the email to be sent.
"""

import psutil  # PSUtil module for the system scanning.
import config  # Config module for access to the settings.
import mail  # Mail module for email sending.
import prettytable  # Prettytable module for the status report.
import os  # Os module for the current directory and 'isfile' function.
import json  # JSON module for the Json manipulation.
import util_funcs as utils  # Utils module for the utility functions.


def check_property(prop):
    """
    Check whether a property is supported on the current system.
    Useful for fans and thermostats.
    :param prop: The property to check.
    :return: Property's value, if supported. Otherwise None.
    """
    if hasattr(psutil, prop):
        return getattr(psutil, prop)()
    return None


def scan_processes():
    """
    Checks the status of all processes set in the config file.
    :return: Dict containing the statuses of all set processes.
    """

    def check_process(name):
        """
        Checks whether a process matching the parameter name is running.
        :param name: The name of the process to check.
        :return: Boolean, indicating whether a process is running (True) or not (False).
        """
        for p in psutil.process_iter(attrs=['name']):
            if p.info['name'] == name:
                return True
        return False

    result = {}
    for process in config.settings["alerts"]["processes"]:
        if not check_process(process):
            result[process] = False
    return result


def system_scan():
    result = {
        "processes": scan_processes(),
    }
    if config.settings["alerts"]["cpu_percent"] > -1:
        result["cpu"] = psutil.cpu_percent(interval=1)  # interval must be set to >0 in order to avoid '0.0' as return
    if config.settings["alerts"]["memory_percent"] > -1:
        result["memory"] = psutil.virtual_memory()[2]  # 3rd cell contains the percentage use
    if config.settings["alerts"]["swap_percent"] > -1:
        result["swap"] = psutil.swap_memory()[3]  # 4th cell contains the percentage use
    if config.settings["alerts"]["temp_core"] > -1:
        result["temp"] = check_property("sensors_temperatures")

    return result


def check_status():
    """
    Performs a system scan.
    Checks the status of each individual parameter against it's setting in the config file.
    If the value is not in the correct threshold, an alert will be generated.
    Additionally, performs the logging of the events.
    :return: Dict, containing the updated system status (alerts only).
    """

    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Timestamp
    timestamp = utils.timestamp

    """Logger"""
    logger = utils.logger()

    """Last known system status"""
    if os.path.isfile("{}/status.json".format(dir_path)):
        with open("{}/status.json".format(dir_path), "r") as f:
            prev_status = json.loads(f.read())
    else:
        prev_status = {}

    """System scan"""
    # The results of the system scan.
    sys_scan = system_scan()

    """Current system status"""
    # Declare the current system status dict, with nested dicts.
    cur_status = {}

    """Resolved alerts"""
    # A list of all the resolved alerts
    cur_status["resolved"] = []

    """Processes"""
    # If the 'prev_status' dict has no 'processes' key in it:
    if "processes" not in prev_status:
        # Create such a key with an empty dictionary.
        prev_status["processes"] = {}

    # Iterate over the results of the processes scan.
    for process in sys_scan["processes"]:
        # Add the 'processes' key to enable it's nested population.
        if "processes" not in cur_status:
            cur_status["processes"] = {}
        # If the process was already logged as down:
        if process in prev_status["processes"]:
            # If more than hour passed since the alert's report:
            if utils.time_since_report(prev_status["processes"][process]):
                # Update the 'updated' value and the 'reported' value to the current timestamp.
                cur_status["processes"][process] = {"triggered": prev_status["processes"][process]["triggered"],
                                                    "updated": timestamp, "reported": timestamp}
            else:
                # Otherwise only update the 'updated' field.
                cur_status["processes"][process] = {"triggered": prev_status["processes"][process]["triggered"],
                                                    "updated": timestamp,
                                                    "reported": prev_status["processes"][process]["reported"]}
        # If the process just stopped.
        else:
            # Create a new entry with the trigger time set to current time and same time for update and report time.
            cur_status["processes"][process] = {"triggered": timestamp, "updated": timestamp, "reported": timestamp}
            # Add a message to the text log, indicating that the process is down.
            logger.warning("Process {} is DOWN.".format(process))

    # Detect processes that were down but are up now.
    # Iterate over the processes in the last know status.
    for process in prev_status["processes"]:
        # If the logged process is not in the current system scan:
        if process not in sys_scan["processes"]:
            # Add the name of the process to the resolved alerts list
            cur_status["resolved"].append(process)
            # Add a message to the text log, indicating that the process is up.
            logger.info("Process {} is UP.".format(process))

    """CPU"""
    # If the CPU value is above it's alert threshold:
    if "cpu" in sys_scan and sys_scan["cpu"] > config.settings["alerts"]["cpu_percent"]:
        # If the cpu alert was already logged:
        if "cpu" in prev_status:
            # If more than hour passed since the alert's report:
            if utils.time_since_report(prev_status["cpu"]):
                # Update the 'updated' value and the 'reported' value to the current timestamp.
                cur_status["cpu"] = {"value": sys_scan["cpu"], "triggered": prev_status["cpu"]["triggered"],
                                     "updated": timestamp, "reported": timestamp}
            else:
                # Otherwise only update the 'updated' field.
                cur_status["cpu"] = {"value": sys_scan["cpu"], "triggered": prev_status["cpu"]["triggered"],
                                     "updated": timestamp, "reported": prev_status["cpu"]["reported"]}
        # If the alert was just generated.
        else:
            # Create a new entry with the trigger time set to current time and same time for update and report time.
            cur_status["cpu"] = {"value": sys_scan["cpu"], "triggered": timestamp, "updated": timestamp,
                                 "reported": timestamp}
            # Add a message to the text log, indicating that the value is above it's threshold.
            logger.warning("CPU load is beyond the alert threshold.")
    # If the CPU value is normal:
    else:
        # If the cpu alert was already logged:
        if "cpu" in prev_status:
            # Add the name of the property to the resolved alerts list
            cur_status["resolved"].append("cpu")
            # Add a message to the text log, indicating that the value is below it's threshold.
            logger.info("CPU load is below the alert threshold.")

    """Memory"""
    # If the memory value is above it's alert threshold:
    if "memory" in sys_scan and sys_scan["memory"] > config.settings["alerts"]["memory_percent"]:
        # If the memory alert was already logged:
        if "memory" in prev_status:
            # If more than hour passed since the alert's report:
            if utils.time_since_report(prev_status["memory"]):
                # Update the 'updated' value and the 'reported' value to the current timestamp.
                cur_status["memory"] = {"value": sys_scan["memory"], "triggered": prev_status["memory"]["triggered"],
                                        "updated": timestamp, "reported": timestamp}
            else:
                # Otherwise only update the 'updated' field.
                cur_status["memory"] = {"value": sys_scan["memory"], "triggered": prev_status["memory"]["triggered"],
                                        "updated": timestamp, "reported": prev_status["memory"]["reported"]}
        # If the alert was just generated.
        else:
            # Create a new entry with the trigger time set to current time and same time for update and report time.
            cur_status["memory"] = {"value": sys_scan["memory"], "triggered": timestamp, "updated": timestamp,
                                    "reported": timestamp}
            # Add a message to the text log, indicating that the value is above it's threshold.
            logger.warning("Memory load is beyond the alert threshold.")
    # If the memory value is normal:
    else:
        # If the memory alert was already logged:
        if "memory" in prev_status:
            # Add the name of the property to the resolved alerts list
            cur_status["resolved"].append("memory")
            # Add a message to the text log, indicating that the value is below it's threshold.
            logger.info("Memory load is below the alert threshold.")

    """Swap"""
    # If the swap memory value is above it's alert threshold.
    if "swap" in sys_scan and sys_scan["swap"] > config.settings["alerts"]["swap_percent"]:
        # If the swap memory alert was already logged:
        if "swap" in prev_status:
            # If more than hour passed since the alert's report:
            if utils.time_since_report(prev_status["swap"]):
                # Update the 'updated' value and the 'reported' value to the current timestamp.
                cur_status["swap"] = {"value": sys_scan["swap"], "triggered": prev_status["swap"]["triggered"],
                                      "updated": timestamp, "reported": timestamp}
            else:
                # Otherwise only update the 'updated' field.
                cur_status["swap"] = {"value": sys_scan["swap"], "triggered": prev_status["swap"]["triggered"],
                                      "updated": timestamp, "reported": prev_status["swap"]["reported"]}
        # If the alert was just generated.
        else:
            # Create a new entry with the trigger time set to current time and same time for update and report time.
            cur_status["swap"] = {"value": sys_scan["swap"], "triggered": timestamp, "updated": timestamp,
                                  "reported": timestamp}
            # Add a message to the text log, indicating that the value is above it's threshold.
            logger.warning("Swap memory load is beyond the alert threshold.")
    # If the swap memory value is normal:
    else:
        # If the memory alert was already logged:
        if "swap" in prev_status:
            # Add the name of the property to the resolved alerts list
            cur_status["resolved"].append("swap")
            # Add a message to the text log, indicating that the value is below it's threshold.
            logger.info("Swap memory load is below the alert threshold.")

    """Temperature"""
    # On some VMs there are no thermostats at all ;)
    if type(sys_scan["temp"]) is dict and "coretemp" in sys_scan["temp"]:
        # If the temperature value is above it's alert threshold.
        if sys_scan["temp"]["coretemp"][0][1] > config.settings["alerts"]["temp_core"]:
            # Add the 'temp' key to enable it's nested population.
            if "temp" not in cur_status:
                cur_status["temp"] = {}
            # If the temperature alert was already logged:
            if "temp" in prev_status:
                # If more than hour passed since the alert's report:
                if utils.time_since_report(prev_status["temp"]):
                    # Update the 'updated' value and the 'reported' value to the current timestamp.
                    cur_status["temp"] = {
                        "value": sys_scan["temp"]["coretemp"][0][1],
                        "triggered": prev_status["temp"]["triggered"], "updated": timestamp,
                        "reported": timestamp
                    }
                else:
                    # Otherwise only update the 'updated' field.
                    cur_status["temp"] = {
                        "value": sys_scan["temp"]["coretemp"][0][1],
                        "triggered": prev_status["temp"]["triggered"], "updated": timestamp,
                        "reported": prev_status["temp"]["reported"]
                    }
            # If the alert was just generated.
            else:
                # Create a new entry with the trigger time set to current time and same time for update and report time.
                cur_status["temp"] = {
                    "value": sys_scan["temp"]["coretemp"][0][1],
                    "triggered": timestamp, "updated": timestamp, "reported": timestamp
                }
                # Add a message to the text log, indicating that the value is above it's threshold.
                logger.warning("Temperature is beyond the alert threshold.")
        # If the temperature value is normal:
        else:
            # If the temperature alert was already logged:
            if "temp" in prev_status:
                # Add the name of the property to the resolved alerts list
                cur_status["resolved"].append("temp")
                # Add a message to the text log, indicating that the value is below it's threshold.
                logger.info("Temperature is below the alert threshold.")

    return cur_status


def save_report(log_data):
    """
    Saves the status report to a JSON file.
    :param log_data: The log to be saved.
    :type log_data: Dict
    :return: None
    :raises TypeError: If the parameter is not a Dict.
    """

    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if type(log_data) is dict:
        json_data = json.dumps(log_data, indent=4, sort_keys=True)
        # Create the file if it doesn't exist.
        with open("{}/status.json".format(dir_path), "w+") as f:
            f.write(json_data)
    else:
        raise TypeError("Parameter must be a dictionary!")


def read_log():
    """
    Reads the log file and prints it on the screen.
    :return: None
    """
    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.isfile("{}/status.json".format(dir_path)):
        print "The log is empty"
    else:
        with open("{}/status.json".format(dir_path), "r") as f:
            print f.read()


def print_report():
    """
    Prints the current system's status report in a human readable form.
    Organizes the data as a table.
    :return: None
    """
    status_report = check_status()
    table = prettytable.PrettyTable()
    table._set_field_names(["Alert", "Triggered at", "Duration"])
    table.hrules = prettytable.ALL  # Print horizontal borders after each line.

    if "processes" in status_report:
        for process in status_report["processes"]:
            table.add_row(
                ["Process {} is not running!".format(process),
                 status_report["processes"][process]["triggered"], utils.duration(status_report["processes"][process])]
            )

    if "cpu" in status_report:
        table.add_row(
            ["CPU use is too high! Current: {}, Alert: {}".format(status_report["cpu"]["value"],
                                                                  config.settings["alerts"]["cpu_percent"]),
             status_report["cpu"]["triggered"], utils.duration(status_report["cpu"])]
        )

    if "memory" in status_report:
        table.add_row(
            ["Memory use is too high! Current: {}, Alert: {}".format(status_report["memory"]["value"],
                                                                     config.settings["alerts"]["memory_percent"]),
             status_report["memory"]["triggered"], utils.duration(status_report["memory"])]
        )

    if "swap" in status_report:
        table.add_row(
            ["Swap use is too high! Current: {}, Alert: {}".format(status_report["swap"]["value"],
                                                                   config.settings["alerts"]["swap_percent"]),
             status_report["swap"]["triggered"], utils.duration(status_report["swap"])]
        )

    if "temp" in status_report:
        if "coretemp" in status_report["temp"]:
            table.add_row(
                ["Core temperature is too high! Current: {}, Alert: {}".format(status_report["temp"]["coretemp"],
                                                                               config.settings["alerts"]["temp_core"]),
                 status_report["temp"]["triggered"], utils.duration(status_report["temp"])]
            )

    # Align table elements to left
    table.align = "l"

    print table


def main():
    """
    Runs the system status check and sends alerts to set email.
    :return: None
    """

    def is_reported(entry):
        """
            Receive an alert entry and decide whether a mail needs to be sent.
            :param entry: The alert entry.
            :type entry: Dict
            :return: True if a mail needs to be sent, False otherwise.
            :raises KeyError: In case the dictionary doesn't have the correct keys.
            :raises TypeError: In case the entry is not a dictionary.
            """
        if type(entry) is dict:
            if "reported" in entry and "updated" in entry:
                if entry["reported"] == entry["updated"]:
                    return True
            else:
                raise KeyError("No 'reported' or 'updated' fields in the dict!")
        else:
            raise TypeError("Entry has to be a dictionary!")
        return False

    # The alerts that will be mailed.
    mail_content = []

    status_report = check_status()

    # Check the status report and decide about which alerts a mail needs to be sent.
    # If the reported time == updated time we will send a mail:
    for key in status_report:
        if key == "resolved":
            # Resolved alerts
            for alert in status_report["resolved"]:
                mail_content.append("{} status is resolved.".format(alert))
        # Since 'processes' is a nested dictionary, we need to iterate over it's content.
        elif key == "processes":
            for process in status_report[key]:
                if is_reported(status_report[key][process]):
                    mail_content.append("Process {} is DOWN.".format(process))
        else:
            if is_reported(status_report[key]):
                mail_content.append("{} value is above it's threshold: {}.".format(key, status_report[key]["value"]))

    # If there are any alerts to send:
    if mail_content:
        # The alerts, as a readable string.
        mail_body = "\n".join(mail_content)
        # Debug text, which can be written to a log when the script is ran as a cronjob.
        print "DEBUG: Mail content: {}".format(mail_body)
        mail.send('noreply@me.com', config.settings["email"]["address"], mail_body,
                  config.settings["email"]["smtp_server"])

    # Remove the 'resolved' list from the status report before saving.
    status_report.pop("resolved", None)
    save_report(status_report)


if __name__ == "__main__":
    # In case the script is being ran as a cron job by direct call to the file.
    main()
