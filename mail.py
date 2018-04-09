"""
Email sending module
"""

import smtplib  # Import smtplib for the actual sending function
import config  # Import the config module for the SMTP settings
from email.mime.text import MIMEText  # Import the email modules


def send(sender, to, body, smtp_server):
    # Create a text/plain message (Only ASCII characters work here)
    msg = MIMEText(body)

    msg["Subject"] = "LSM Report"
    msg["From"] = sender
    msg["To"] = to

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP(smtp_server, "2525")

    # If the username and the password are not empty:
    if config.settings["email"]["smtp_user"] and config.settings["email"]["smtp_pass"]:
        # Login before sending
        # Explicit casting to string required by the module
        username = str(config.settings["email"]["smtp_user"])
        password = str(config.settings["email"]["smtp_pass"])
        server.starttls()
        server.login(username, password)

    server.sendmail(sender, [to], msg.as_string())
    server.quit()