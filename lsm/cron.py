from crontab import CronTab  # Crontab module for basic crontab manipulation.
import getpass  # Getpass module for the current username.
import os  # Os module for the current working directory.


def setup():
    """
    Returns the current user's crontab and the current working directory.
    :return: Tuple, containing the information mentioned above.
    """
    # Get current user
    username = getpass.getuser()

    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Get the user's personal crontab
    user_cron = CronTab(user=username)

    # Return the crontab and the directory path
    return user_cron, dir_path


def add():
    """
    Adds the 'monitor.py' to the crontab to execute every minute.
    :return: None
    """
    # Get the crontab and the current working directory
    user_cron, dir_path = setup()

    # Set a task
    task = user_cron.new(command="cd {} && python monitor.py".format(dir_path), comment="lsm")

    # Set run frequency
    task.minute.every(1)

    # Write to crontab
    user_cron.write()


def remove():
    """
    Removes the 'monitor.py' command form the user's crontab.
    This is done by selecting all jobs with the 'lsm' comment.
    :return: None
    """
    # Get the user's crontab
    user_cron = setup()[0]

    # Remove the task by it's ID (comment)
    user_cron.remove_all(comment="lsm")

    # Write to crontab
    user_cron.write()


def is_set():
    """
    Checks whether the cronjob is set in the user's crontab.
    This is done by checking for jobs with the 'lsm' comment.
    :return: None
    """
    # Get the user's crontab
    user_cron = setup()[0]

    # Iterate over tasks
    for task in user_cron:
        # If a task with a comment 'lsm' is found:
        if task.comment == "lsm":
            # Return True, as in the task is set.
            return True

    # Otherwise return false.
    return False
