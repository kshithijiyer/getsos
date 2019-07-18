#!/usr/bin/python3
"""
    getsos
    Description: A tool to collect sosreports of multiple servers.
    Author: Kshithij Iyer
    Date: 3/11/2018
    Email: kshithij.ki@gmail.com
"""

# Imports needed by the script.
import argparse
import os
import sys
from version import __version__


def read_config_file(config_file):
    """
    A function to read config file and create a list of servers.
    Args:
        config_file: A file which has all the servers' IP/hostnames.
    Returns:
        list: A list of all servers.
    """
    try:
        config_file = open(config_file, 'r')
        print("[INFO]:Reading config details from %s." % config_file.name)
        list_of_servers = []
        lines_of_config_file = config_file.readlines()
        print("[INFO]:Creating list of servers from config file.")
        for line in lines_of_config_file:
            list_of_servers = (list_of_servers +
                                line.replace("\n", "")
                                .replace(" ", "").split(","))
        print("[INFO]:Removing blank values from list.")
        while '' in list_of_servers:
            list_of_servers.remove('')
        print("[INFO]:Closing config file.")
        config_file.close()
        return list_of_servers

    except FileNotFoundError:
        sys.exit("[ERROR]:Configuration file not found!")


def remove_pervious_sosreports(server, username):
    """
    A function to remove old sosreports.
    Args:
        server: hostname/IP server from which sosreport
                has to be removed.
        username: User to be used to login.
    Returns:
        bool: True if successful else false.
    """
    command = ("ssh %s@%s \"rm -rf /var/tmp/sosreport-*\""
               % (username, server))
    ret = os.system(command)
    if ret:
        return False
    return True


def collect_new_sosreports(server, username):
    """
    A function to generate sosreports.
    Args:
    server: hostname/IP server from which sosreport
            has to be collected.
    username: User to be used to login.      
    Returns:
        bool: True if successful else false.
    """
    command = ("ssh %s@%s \"yes | sosreport\""
               % (username, server))
    ret = os.system(command)
    if ret:
        return False
    return True


def setup_passwordless_ssh(server, username, password):
    """
    A function to setup passwordless ssh to all servers.
    Args:
    server: hostname/IP of server for passwordless ssh
            has to be configured.
    username: User to be used to login.
    password: password to be used to login.
    Returns:
        bool: True if successful else false.
    """
    command = ("sshpass -p %s ssh-copy-id %s@%s"
               % (password, username, server))
    ret = os.system(command)
    if ret:
        return False
    return True


def copy_sosreports_to_dir(server, username, directory):
    """
    A function to copy sosreports to local dir.
    Args:
    server: hostname/IP of server for passwordless ssh
            has to be configured.
    username: User to be used to login.
    directory: Directory to be used to store sosreports.
    Returns:
        bool: True if successful else false.
    """
    command = ("scp %s@%s:/var/tmp/sosreport-* %s"
               % (username, server, directory))
    ret = os.system(command)
    if ret:
        return False
    return True


def check_and_create_dir_if_not_present(directory):
    """
    A function to check and create directory if not present.
    Args:
    directory: Directory to be checked/created.
    Returns:
        bool: True if successful else false.
    """
    if not os.path.isdir(directory):
        command = ("mkdir -p %s" % directory)
        ret = os.system(command)
        if ret:
            return False
    else:
        print("[INFO]:The dir already exists.")
    return True


def main():
    """
    Main function of the tool.
    """

    # Setting up command line arguments.
    parser = argparse.ArgumentParser(
        description="A tool to collect sosreports of multiple servers."
        )
    parser.add_argument("-f",
                        "--config_file",
                        type=str,
                        dest="config_file",
                        help="File with list of ips/hostnames of servers.")
    parser.add_argument("-m", "--servers", type=str,
                        dest="servers",
                        help=("A list of hostnames/ips of"
                              " servers seperated by comma(',')."))
    parser.add_argument("-d", "--dist-dir", type=str, default=".",
                        dest="directory",
                        help=("Directory where reports have to be stored."
                        "(Default:.)"))
    parser.add_argument("-u", "--username", type=str,
                        default="root", dest="username",
                        help="Username to login into servers.(default:root)")
    parser.add_argument("-p", "--password", dest="password",
                        help="Password of servers.")
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version="%(prog)s {version}".format(version=__version__)
                        )
    args = parser.parse_args()

    # Getting list of hostname/IP.
    if args.servers:
        servers = args.servers.split(',')

    # Reading the config file.
    if args.config_file:
        servers = read_config_file(args.config_file)

    # Fetching other parameters from command line.
    username = args.username
    directory = args.directory
        
    # Checking and creating dir if not present.
    ret = check_and_create_dir_if_not_present(directory)
    if not ret:
        sys.exit("[ERROR]:Unable to create dir for storing sosreports.")

    try:
        for server in servers:

            # If password is provided setup passwordless SSH.
            if args.password:
                ret = setup_passwordless_ssh(server, username,
                                             args.password)
                if not ret:
                    sys.exit("[ERROR]:Unable to setup passwordless ssh.")
                print("[INFO]:Passwordless ssh setup complete!")

            # Removing old sosreports from the server.
            ret = remove_pervious_sosreports(server, username)
            if not ret:
                sys.exit("[ERROR]:Unable to remove old sosreports on %s!"
                         % server)
            print("[INFO]:Successfully removed old sosreports on %s."
                  % server)

            # Collecting sosreport on the server.
            ret = collect_new_sosreports(server, username)
            if not ret:
                sys.exit("[ERROR]:Unable to collect sosreport on %s!"
                         % server)
            print("[INFO]:Successfully collected sosreport on %s."
                  % server)

            # Downloading sosreport to local machine.
            ret = copy_sosreports_to_dir(server, username, directory)
            if not ret:
                sys.exit("[ERROR]:Unable download sosreport from %s."
                         % server)
            print("[INFO]:Successfully copied sosreports from %s." % server)

    # If configuration is not provided. 
    except UnboundLocalError:
        sys.exit("[ERROR]:servers were not provided")

if __name__ == "__main__":
    main()
