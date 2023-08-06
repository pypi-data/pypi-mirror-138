#!/usr/bin/env python

import subprocess # for execute cammands
import optparse #for option in terminal
import re

def get_arguments():
    parser=optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface To change Its MAC Address")
    parser.add_option("-m","--mac",dest="mac_add",help="New MAC Address")
    (option,arguments)= parser.parse_args()
    if not option.interface:
        parser.error("[-] Please Specify The Interface, use --help For More Info..")
    elif not option.mac_add:
        parser.error("[-] Please Specify The MAC Address, use --help For More Info..")
    return option

def change_mac(interface,mac_add):
    print(" [+] Changing MAC Address For " + interface + " to "+ mac_add )
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",mac_add])
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac(interface):
    ifconfig_results=subprocess.check_output(["ifconfig",interface])
    mac_add_search_results=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_results.decode())
    if mac_add_search_results:
        return mac_add_search_results.group(0)
    else:
        print("[-] Could not found MAC Address.")
# call
def main():
    option = get_arguments()
    current_mac=get_current_mac(option.interface)
    print("current MAC = " + str(current_mac))
    change_mac(option.interface,option.mac_add)
    current_mac=get_current_mac(option.interface)
    if current_mac == option.mac_add:
        print("[+] MAC Address was Successfully Changed to " + current_mac)
    else:
        print("[-] MAC Address Did Not Changed.")


if __name__ == "__main__":
    main()