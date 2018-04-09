# LSM
Light System Monitor

A system monitor tool that is designed to be ran as a cronjob, will watch for the configured events and thresholds and send alerts to the set email address.

## Installation

Installation is simple.
1. Clone or download the repository to your machine.
2. Run `lsm.py`.
3. Add to the user's personal crontab via the interactive mode or the `lsm.py -f --cronadd` command.

## Configuration

Configuration is stored in the `config.json` file.
It is very simple and intuitive, threshold values are set for parameters such a CPU percentage load
and the processes to be watched are only mentioned by their name.

Additionally, it is possible to change the configuration via the application's interactive and flag modes.

## Usage

* `lsm.py -h` for the help window.
* `lsm.py -i` for the interactive mode that features multichoice menus.
* `lsm.py -f` for the flags mode, that enables quick access to the desired function.
