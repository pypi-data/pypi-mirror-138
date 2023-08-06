import platform
import sys
import os
import json
import subprocess
from pathlib import Path
import clointfusion.resources as data

user_name = os.getlogin()
windows_os = "windows"
linux_os = "linux"
mac_os = "darwin"
os_name = str(platform.system()).lower()
user_name = os.getlogin()
user_email = ""

python_version = str(sys.version_info.major) + "." + \
    str(sys.version_info.minor)
python_37 = "3.7"
python_38 = "3.8"
python_39 = "3.9"
python_310 = "3.10"
restart = False

python_exe_path_ut = os.path.join(os.path.dirname(sys.executable), "python.exe")
pythonw_exe_path_ut = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")

python_exe_path = python_exe_path_ut.replace(" ", '" "')
pythonw_exe_path = pythonw_exe_path_ut.replace(" ", '" "')

browser_driver = ""
helium_service_launched = False

data_folder = data.__path__[0]

cf_icon_file_path = Path(os.path.join(data_folder, "Cloint-ICON.ico"))
data_json_file = Path(os.path.join(data_folder, "data.json"))
cf_icon_cdt_file_path = Path(os.path.join(data_folder, "Cloint-ICON-CDT.ico"))
cf_logo_file_path = Path(os.path.join(data_folder, "Cloint-LOGO.PNG"))


def _welcome_to_clointfusion():
    from pyfiglet import Figlet
    from rich.console import Console
    import datetime
    import random

    console = Console()
    """
    Internal Function to display welcome message & push a notification to ClointFusion Slack
    """
    version = "(Version: 1.1.4)"

    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 16:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    messages_list = ['Where would I be without a friend like you?', 'I appreciate what you did.',
                     'Thank you for thinking of me.', 'Thank you for your time today.',
                     'I am so thankful for what you did here', 'I really appreciate your help. Thank you.',
                     "You know, if you're reading this, you're in the top 1% of smart people.",
                     'We know the world is full of choices. Yet you picked us, Thank you very much.',
                     'Thank you. We hope your experience was excellent and we can’t wait to see you again soon.',
                     'We hope you are happy with our tool, if not we are just an e-mail away at '
                     'clointfusion@cloint.com. We will be pleased to hear from you.',
                     'ClointFusion would like to thank excellent users like you for your support. We couldn’t do it '
                     'without you!',
                     'Thank you for your business, your trust, and your confidence. It is our pleasure to work with '
                     'you.',
                     'We take pride in your business with us. Thank you!',
                     'It has been our pleasure to serve you, and we hope we see you again soon.',
                     'We value your trust and confidence in us and sincerely appreciate you!',
                     'Your satisfaction is our greatest concern!', 'Your confidence in us is greatly appreciated!',
                     'We are excited to serve you first!',
                     'Thank you for keeping us informed about how best to serve your needs. Together, we can make '
                     'this history.',
                     'Our brand innovation wouldn’t have been possible if you didn’t give us feedback about our '
                     'services.',
                     'Thank you so much for playing a pivotal role in our growth. We’ll make sure we continue to put '
                     'your needs first as our company expands and improves.',
                     'We are exceedingly pleased to find people we can always count on. Thank you for being one of '
                     'our loyal and trusted clients.', ]
    message = random.choice(messages_list)
    welcome_msg = f"\n{greeting} {str(user_name).title()} !  Welcome to ClointFusion, Made in India with ❤️"
    # print_with_magic_color(welcome_msg,magic=True)
    print(welcome_msg)
    print()
    print(message)
    f = Figlet(font='small', width=150)
    console.print(f.renderText("ClointFusion Community Edition"))
    # env_var_verify()
    # scripts_verify()

# check the system and return true if 64 bit, false if 32 bit

def is_supported():
    import struct
    import sys

    bit_size = struct.calcsize("P") * 8
    if bit_size == 32:
        print("We don't support 32-bit Architecture")
        print(
            "Please download 64-bit Architecture from the link down below. Press (ctrl + click) on link to download.\n")
        if os_name == "windows":
            print("https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe")
        if os_name == "darwin":
            print("https://www.python.org/ftp/python/3.9.7/python-3.9.7-macos11.pkg")
        sys.exit(0)
    else:
        return True


def report_error(message: Exception):
    from clointfusion.exception_handler import centralized_exception_hanlder
    centralized_exception_hanlder(message)


def env_var_verify():
    global restart
    key = 'ClointFusionCE'
    try:
        enviro_var = os.environ[key]
        if python_exe_path_ut.lower() == enviro_var.lower():
            return True
        else:
            subprocess.call(f'setx {key} "{python_exe_path_ut}"',
                            stdout=subprocess.PIPE, shell=True)
            restart = True
            return True
    except KeyError:
        subprocess.call(f'setx {key} "{python_exe_path_ut}"',
                        shell=True, stdout=subprocess.PIPE)
        restart = True
        return True
    except Exception as e:
        report_error(e)
        return False


def scripts_verify():
    global restart
    Scripts_Path = os.path.join(sys.exec_prefix, "Scripts")
    user_path = (str(subprocess.run(
        ["powershell", "-Command", "[Environment]::GetEnvironmentVariable('Path','User')"], capture_output=True).stdout.decode('ascii')).replace(
        ';;', ';')).replace('\r\n', '')
    if Scripts_Path.lower() not in user_path.lower():
        user_path = user_path + ';' + Scripts_Path + ';' + '\r\n'
        subprocess.call('setx path "{}"'.format(user_path),
                        shell=True, stdout=subprocess.PIPE)
        restart = True


def is_connected(hostname):
    try:
        import socket
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


if os_name == windows_os:
    if os_name == windows_os and sys.argv[0].endswith(('cf_py.exe', 'cf.exe')):
        # Add cli's here to skip the welcome msg twice
        pass
    else:
        # if is_connected("one.one.one.one"):
        #     from clointfusion.verify import verify_with_server
        
        #     status, data = verify_with_server()
        #     if status:
        #         user_name = data['name']
        #         user_email = data['email']
        # else:
        #     data_path = os.path.join(data_folder, "data.json")
        #     with open(data_path, "r") as file:
        #         data = json.load(file)
        #     user_name = data['name']
        #     user_email = data['email']
        #     print("To experience the full ClointFusion experience, please connect to internet. Some of the features may not work properly.")

        _welcome_to_clointfusion()
        
        # if restart == True:
        #     import PySimpleGUI as sg
        #     sg.theme('DarkBlue')
        #     print("Settings Updated. Please restart the program.")
        #     # ask to restart
        #     resp = sg.popup_ok_cancel(
        #         "Restart the system to apply changes. \nClick 'OK' to restart. \n \nMake sure you saved your progress before proceeding", title="Settings Updated")
        #     if resp == "OK":
        #         resp = sg.PopupAutoClose("Restarting...\n\nPress CANCEL to stop Restarting.\n", auto_close_duration=5, button_type=sg.POPUP_BUTTONS_OK_CANCEL)
        #         if resp == "Cancel":
        #             sys.exit()
        #         os.system("shutdown /r /t 0")


elif os_name == linux_os:
    pass

elif os_name == mac_os:
    pass

else:
    pass

