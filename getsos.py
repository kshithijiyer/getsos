#!/usr/bin/python
"""
    getsos 
    Description: A tool to collect sosreports of multiple machines.
    Author: Kshithij Iyer
    Date: 3/11/2018 
    Email: kshithij.ki@gmail.com
"""

#imports needed by the script.
import argparse, os, sys
from version import __version__

def read_config_file(config_file):
    """
        A function to read config file and create a list of machines
    """
    try:
        config_file=open(config_file,'r')
        print("[INFO]:Reading from",config_file.name,"config file.")
        list_of_machines = []
        lines_of_config_file = config_file.readlines()
        print("[INFO]:Creating list of machines from config file.")
        for line in lines_of_config_file:
            list_of_machines = (list_of_machines +
                                line.replace("\n","").replace(" ","").split(","))
        print("[INFO]:Removing blank values from list.")
        while '' in list_of_machines:
            list_of_machines.remove('')
        print("[INFO]:Closing config file.")
        config_file.close()
        return list_of_machines

    except FileNotFoundError:
        sys.exit("[ERROR]:Configuration file not found!")
     
def remove_pervious_sosreports(machine,username):
    """
        A function to remove old sosreports.
    """
    command = "ssh "+username+"@"+machine+" \"rm -rf /var/tmp/sosreport-*\""
    ret = os.system(command) 
    if ret:
        return False
    return True

def collect_new_sosreports(machine,username):
    """
        A function to generate sosreports.
    """
    command = "ssh "+username+"@"+machine+" \"yes | sosreport\""
    ret = os.system(command) 
    if ret:
        return False
    return True

def copy_sosreports_to_dir(machine,username,directory):
    """
        A function to copy sosreports to local dir.
    """
    command = "scp "+username+"@"+machine+":/var/tmp/sosreport-* "+directory+" "
    ret = os.system(command)
    if ret:
        return False
    return True

def check_and_create_dir_if_not_present(directory):
    """
        A function to check and create directory if not present.
    """
    if not os.path.isdir(directory):
        command = "mkdir -p "+directory
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
    parser=argparse.ArgumentParser(description="A tool to collect sosreports of multiple machines.")
    parser.add_argument('-f', "--config_file", type=str,
                        dest="config_file",
                        help="File with list of ips/hostnames of machines.")
    parser.add_argument('-m',"--machines", type=str,
                        dest="machines",
                        help="A list of hostnames/ips of machines seperated by comma(',').")
    parser.add_argument('-d', "--dist-dir", type=str,default=".",
                        dest="directory",
                        help="Path to dir where all reports have to be stored.(default:.)")
    parser.add_argument('-u', "--username", type=str,default="root",
                        dest="username",
                        help="Username to login into machines.(default:root)")
    parser.add_argument('-v', '--version' ,action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    args=parser.parse_args()

    # Getting list of hostname/ipes
    if args.machines:
        machines = args.machines.split(',') 

    # Reading the config file.
    if args.config_file:
        machines = read_config_file(args.config_file)

    # Fetching other parameters from command line
    username = args.username
    directory = args.directory

    ret = check_and_create_dir_if_not_present(directory)
    if not ret:
        sys.exit("[ERROR]:Unable to create dir for storing sosreports.")
    try:
        for machine in machines:

            ret = remove_pervious_sosreports(machine,username)
            if not ret:
                sys.exit("[ERROR]:Unable to remove old sosreports on "+machine+"!")
            print("[INFO]:Successfully removed old sosreports on "+machine+".")

            ret = collect_new_sosreports(machine,username)
            if not ret:
                sys.exit("[ERROR]:Unable to collect sosreport on "+machine+"!")
            print("[INFO]:Successfully collected sosreport on "+machine+".")

            ret = copy_sosreports_to_dir(machine,username,directory)
            if not ret:
                sys.exit("[ERROR]:Unable to copy sosreport from "+machine+" to loaclhost!")
            print("[INFO]:Successfully copied sosreports from "+machine+".")
    except UnboundLocalError:
        sys.exit("[ERROR]:Machines were not provided")

if __name__ == "__main__":
   main()
