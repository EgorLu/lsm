"""
Utility functions module.
"""

import logging  # Import the logging module to manage the log.
from datetime import datetime  # Import the datetime for the timestamp.

# Timestamp
timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def logger():
    logger = logging.getLogger(__name__)  # Create Logger instance
    handler = logging.FileHandler("./system.log")  # Create a FileHandler
    formatter = logging.Formatter("%(asctime)s %(levelname)8s %(message)s", "%d-%m-%Y %H:%M:%S")  # Create a Formatter
    handler.setFormatter(formatter)  # Attach the Formatter to the FileHandler
    logger.addHandler(handler)  # Attach the FileHandler to the Logger
    logger.setLevel(logging.INFO)  # Set debug level

    return logger


def time_since_report(entry):
    """
    Calculates the time difference between the reported time of the event and its updated time.
    :param entry: A dict with a 'reported' and 'updated' keys that contain datetime objects.
    :type entry: Dict
    :return: Boolean, True in case the time difference is greater than one hour. False otherwise.
    :raises TypeError: In case the parameter is not a dictionary.
    :raises KeyError: In case the parameter doesn't have the correct keys.
    """
    if type(entry) is dict:
        if "reported" in entry:
            reported = datetime.strptime(entry["reported"], "%d-%m-%Y %H:%M:%S")
        else:
            raise KeyError("No 'reported' key in the dict!")
        if "updated" in entry:
            updated = datetime.strptime(entry["updated"], "%d-%m-%Y %H:%M:%S")
        else:
            raise KeyError("No 'updated' key in the dict!")
        delta = updated - reported
        return delta.seconds / 3600 >= 1
    else:
        raise TypeError("Parameter must be a dictionary!")


def duration(entry):
    """
    Calculates the time difference between the triggered time of the event and it's updated time.
    :param entry: A dict with a 'triggered' and 'updated' keys that contain datetime objects.
    :type entry: Dict
    :return: A human readable string representing the time difference between the two events.
    :raises TypeError: In case the parameter is not a dictionary.
    :raises KeyError: In case the parameter doesn't have the correct keys.
    """
    if type(entry) is dict:
        if "triggered" in entry:
            triggered = datetime.strptime(entry["triggered"], "%d-%m-%Y %H:%M:%S")
        else:
            raise KeyError("No 'triggered' key in the dict!")
        if "updated" in entry:
            updated = datetime.strptime(entry["updated"], "%d-%m-%Y %H:%M:%S")
        else:
            raise KeyError("No 'updated' key in the dict!")
        delta = updated - triggered
        result = "{} days, {}:{}:{}".format(delta.days, delta.seconds / 3600, (delta.seconds / 60) % 60,
                                            delta.seconds % 60)
        return result
    else:
        raise TypeError("Parameter must be a dictionary!")
