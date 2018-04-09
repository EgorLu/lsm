"""
Arguments parsing module
"""

from argparse import ArgumentParser  # Main argument parser
from argparse import RawTextHelpFormatter  # Formatter for the help text
import sys  # Sys module for the arguments list


def parse():
    """
    Parse the arguments with which the application was called.
    :return: An object containing the arguments (<argparse.Namespace>)
    """

    # Application description
    description = "Light System Monitor\n" \
                  "Monitors the system's processes and utilization.\n" \
                  "Installs as a cron job and sends alerts via SMTP."

    parser = ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-i", "--interactive", action="store_true",
        help="Interactive mode"
    )
    mode.add_argument(
        "-f", "--flags", action="store_true",
        help="Flags mode"
    )
    parser.add_argument(
        "-r", "--report", action="store_true",
        help="Send a system report to the set email"
    )
    parser.add_argument(
        "-s", "--status", action="store_true",
        help="Display the current status of the system"
    )
    parser.add_argument(
        "-l", "--log", action="store_true",
        help="Display the alert history"
    )
    parser.add_argument(
        "--cronadd", action="store_true",
        help="Add to the user's personal crontab"
    )
    parser.add_argument(
        "--cronremove", action="store_true",
        help="Remove from the user's personal crontab"
    )
    parser.add_argument(
        "--email",
        help="Set email address"
    )
    parser.add_argument(
        "--smtp",
        help="Set smtp server"
    )
    # If no arguments were provided, display the help message
    if len(sys.argv) == 1:
        # print_help takes a stream as a parameter.
        # As a good user interface etiquette,
        # and to stay in line with the rest of the error handling in argsparse,
        # I pass sys.stderr as a parameter.
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()
