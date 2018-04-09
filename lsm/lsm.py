#!/usr/bin/python
"""
    Light System Monitor

Installs as a cron job or can be ran manually in order to scan the system based on preset configuration.
Keeps a log of the events and is able to send email alerts upon alert generation or resolution.
"""

# Imports
import args  # Args module for argument manipulation.
import menu  # Menu module for the interactive mode.
import sys  # Sys module for the 'exit' function.
import os  # Os module for the 'clear' function.
import config  # Config module for the setter functions.
import monitor  # Monitor module for the system report function.
import cron  # Cron module for the add and remove functions.

try:
    # Parse the arguments,
    # then overwrite the 'args' variable with the returned value.
    args = args.parse()

    # Act based on the arguments

    # Interactive mode
    if args.interactive:
        menu.menu_main()

    # Flags mode
    if args.flags:
        # Generate and send a system status report
        if args.report:
            monitor.main()
        # Display the current system status
        if args.status:
            monitor.print_report()
        # Display the history of events
        if args.log:
            monitor.read_log()
        # Add to crontab
        if args.cronadd:
            cron.add()
        # Remove from crontab
        if args.cronremove:
            cron.remove()
        # Quick email change
        if args.email:
            config.set_email(args.email)
        # Quick SMTP server change
        if args.smtp:
            config.set_smtp(args.smtp)

# Gracefully exit on Ctrl+C and Ctrl+D
except (KeyboardInterrupt, EOFError):
    os.system("clear")
    print("Program terminated")
    sys.exit(1)
