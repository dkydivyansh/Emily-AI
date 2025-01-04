import platform
import psutil
import datetime
import sounddevice as sd
import GPUtil
import win32com.client
import sys
import wmi
import os
import ctypes
import subprocess
import socket
import winreg
from ctypes import windll
from urllib.request import urlopen
import cpuinfo
import json


# Defining color codes
black = "\033[0;30m"
red = "\033[0;31m"
bred = "\033[1;31m"
green = "\033[0;32m"
bgreen = "\033[1;32m"
yellow = "\033[0;33m"
byellow = "\033[1;33m"
blue = "\033[0;34m"
bblue = "\033[1;34m"
purple = "\033[0;35m"
bpurple = "\033[1;35m"
cyan = "\033[0;36m"
bcyan = "\033[1;36m"
white = "\033[1;37m"
bwhite = "\033[0;37m"
magenta = "\033[0;35m"
bmagenta = "\033[1;35m"
orange = "\033[38;5;208m" 
bright_red = "\033[91m"
bright_green = "\033[92m"
bright_yellow = "\033[93m"
bright_blue = "\033[94m"
bright_magenta = "\033[95m"
bright_cyan = "\033[96m"
bright_white = "\033[97m"
nc = "\033[00m" 
bright_light_blue = "\033[1;38;2;173;216;230m"
saffron = "\033[38;2;255;153;51m" 
navy_blue = "\033[38;2;0;0;128m" 

nc = "\033[00m" 

version = str("0000")
versioncode = 0000

clear = ('cls' if os.name == 'nt' else 'clear')
con_inf = f'{byellow}[{bmagenta}!{byellow}] {nc}'
con_pls = f'{bgreen}[{bmagenta}+{bgreen}] {nc}'
con_mns = f'{bred}[{bmagenta}-{bred}] {nc}'
con_ai = f'{bgreen}[{bmagenta}✨{bgreen}] {nc}'

logo = f'''{bcyan}
███████╗ ███╗   ███╗ ██╗ ██╗   ██╗   ██╗
██╔════╝ ████╗ ████║ ██║ ██║   ╚██╗ ██╔╝
█████╗   ██╔████╔██║ ██║ ██║    ╚████╔╝ 
██╔══╝   ██║╚██╔╝██║ ██║ ██║     ╚██╔╝  
███████╗ ██║ ╚═╝ ██║ ██║ ███████╗ ██║   
╚══════╝ ╚═╝     ╚═╝ ╚═╝ ╚══════╝ ╚═╝
{bpurple} v{version}{bcyan} By @dkydivyansh{nc}
'''


def print_color_names():
    color_dict = {
        "Black": black,
        "Red": red,
        "Bright Red": bred,
        "Green": green,
        "Bright Green": bgreen,
        "Yellow": yellow,
        "Bright Yellow": byellow,
        "Blue": blue,
        "Bright Blue": bblue,
        "Purple": purple,
        "Bright Purple": bpurple,
        "Cyan": cyan,
        "Bright Cyan": bcyan,
        "White": white,
        "Bright White": bwhite,
        "Magenta": magenta,
        "Bright Magenta": bmagenta,
        "Orange": orange,
        "Bright Red Alt": bright_red,
        "Bright Green Alt": bright_green,
        "Bright Yellow Alt": bright_yellow,
        "Bright Blue Alt": bright_blue,
        "Bright Magenta Alt": bright_magenta,
        "Bright Cyan Alt": bright_cyan,
        "Bright White Alt": bright_white,
        "Saffron": saffron,
        "Navy Blue (Ashoka Chakra)": navy_blue,
        "bright_light_blue" : bright_light_blue
    }

    for color_name, color_code in color_dict.items():
        print(f"{color_code}{color_name}{nc}")


help_dta = f'''
{bgreen}Functions               Uses

{white}Deactivate/Logout            {bcyan}type deactivate_account
{white}Show History                 {bcyan}Show Our History, / type show_history
{white}Clear History                {bcyan}Can You clear history / type erase_memory
{white}Restart                      {bcyan}Can you Restart / type sys_restart
{white}Attach File                  {bcyan}I Want To Attach Files / type attach_file
{white}Scrape Web PAge              {bcyan}scrape <url>, ex. scrape https://dkydivyansh.com and tell summary
{white}Text Method                  {bcyan}Change To Text Method 
{white}Voice Method                 {bcyan}Change To Voice Method / voice_method
{white}Content Generation           {bcyan}Generate/Write/Create Content/Story/Script On <XYZ>
{white}Real-Time Information        {bcyan}What Is Current Time And Date
{white}know your IP                 {bcyan}What Is my ip
{white}know your IP Location        {bcyan}tell my ip Location
{white}know your System Information {bcyan}tell my System Information

{bcyan}You can ask to open - Camera, Calculator, Photo, Gallery, Browser, YouTube, Spotify, WhatsApp, Email, Settings File Manager and Notepad

{bgreen}dkydivyansh.com
{bgreen}Made By Divyansh    Github/@dkydivyansh{nc}
'''


# test 
def verify_system_environment():
    """
    Comprehensive system environment verification for Windows, without requiring admin privileges.
    """
    print("\n=== Starting System Environment Verification ===\n")
    
    verification_results = {
        "status": True,
        "errors": [],
        "warnings": [],
        "system_info": {}
    }

    def check_virtualization():
        """Check if the system is running in a virtual machine"""
        try:
            c = wmi.WMI()
            vm_signs = {
                "manufacturer": ["VMware, Inc.", "VirtualBox", "Microsoft Corporation", "Xen", "KVM", "QEMU"],
                "model": ["Virtual Machine", "VirtualBox", "VMware", "KVM", "Bochs"],
            }
            system = c.Win32_ComputerSystem()[0]
            bios = c.Win32_BIOS()[0]
            
            if any(vm in system.Manufacturer for vm in vm_signs["manufacturer"]):
                return True
            if any(vm in system.Model for vm in vm_signs["model"]):
                return True
            if "VIRTUAL" in bios.SerialNumber.upper():
                return True
        except Exception as e:
            verification_results["warnings"].append(f"Virtualization check failed: {e}")
        return False

    def check_internet_connection():
        """Check internet connectivity by pinging Google's DNS server"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            host = "8.8.8.8"
            command = ['ping', param, '1', '-w', '1000', host]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                if 'time=' in result.stdout.lower():
                    time_str = result.stdout.split('time=')[-1].split('ms')[0].strip()
                    if '<' in time_str:
                        time_str = time_str.replace('<', '')
                    return True, float(time_str), None
                return True, None, None
        except Exception as e:
            return False, None, str(e)
        return False, None, "Ping failed"

    try:
        # Check for virtualization
        print("\n🖥️ Checking Virtualization Status...")
        is_vm = check_virtualization()
        verification_results["system_info"]["virtualization"] = is_vm
        if is_vm:
            verification_results["warnings"].append("Running in virtual environment")

        # BIOS Information
        print("\n📟 Checking BIOS Information...")
        try:
            c = wmi.WMI()
            bios = c.Win32_BIOS()[0]
            verification_results["system_info"]["bios"] = {
                "manufacturer": bios.Manufacturer,
                "version": bios.Version,
                "release_date": bios.ReleaseDate,
                "serial_number": bios.SerialNumber,
                "smbios_version": bios.SMBIOSBIOSVersion
            }
        except Exception as e:
            verification_results["warnings"].append(f"Failed to retrieve BIOS information: {e}")

        # OS Version
        print("\n📊 Checking Operating System...")
        os_info = platform.uname()
        windows_version = platform.win32_ver()
        verification_results["system_info"]["os"] = {
            "name": os_info.system,
            "version": os_info.version,
            "release": os_info.release,
            "build": windows_version[1]
        }

        # Internet Connection
        print("\n🌐 Checking Internet Connection...")
        is_connected, response_time, error = check_internet_connection()
        if is_connected:
            verification_results["system_info"]["internet"] = {
                "status": "Connected",
                "response_time": f"{response_time:.1f}ms" if response_time else "Unknown"
            }
            if response_time and response_time > 100:
                verification_results["warnings"].append(f"High internet latency: {response_time:.1f}ms")
        else:
            verification_results["errors"].append("No internet connection")

        # Final exit code
        exit_code = 0
        if verification_results["errors"]:
            exit_code = 2
            verification_results["status"] = False
        elif verification_results["warnings"]:
            exit_code = 1

        # Overall status
        print("\n=== Final Verification Status ===")
        status_symbol = "✅" if verification_results["status"] else "❌"
        status_text = {
            0: "PASSED",
            1: "PASSED WITH WARNINGS",
            2: "FAILED"
        }
        print(f"\nOverall Status: {status_symbol} {status_text[exit_code]} (Exit Code: {exit_code})")

    except Exception as e:
        verification_results["status"] = False
        verification_results["errors"].append(f"Verification failed: {str(e)}")
        exit_code = 2

    return verification_results, exit_code
