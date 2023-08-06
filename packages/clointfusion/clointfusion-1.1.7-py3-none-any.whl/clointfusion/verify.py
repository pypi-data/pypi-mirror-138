
import tkinter as tk
from tkinter.constants import W
import tkinter.ttk as ttk
import os
import json
import subprocess
import socket
import uuid
import re
import platform
server_ip = "https://web.clointfusion.com/auth"

import clointfusion.resources as resources

data_path = os.path.join(resources.__path__[0], "data.json")
name_logo_path = os.path.join(resources.__path__[0], "CLOINTFUSION.png")
round_logo_path = os.path.join(resources.__path__[0], "CLOINTFUSION_round.png")
name = os.getlogin()
user_email = ''


def get_public_ip(only_ipv4=True):
    # Description:
    """
    Description of the function
    """

    # import section
    import requests

    # Response section
    status = False
    data = None

    try:
        if not only_ipv4:
            data = requests.get('http://ipinfo.io/json').json()
        else:
            public_ip = str(requests.get(
                'https://checkip.amazonaws.com').text.strip())
            data = public_ip

        # If the function returns a value, it should be assigned to the data variable.
        # data = value
    except Exception as e:
        print(e)

    else:
        status = True
    finally:
        if status is True and data is not None:
            return [status, data]
        return [status]

data = get_public_ip(False)[1]

system_uuid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
os_name = str(platform.system()).lower()
public_ip = data['ip']
mac_address = str(':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()
ip_add = socket.gethostbyname(socket.gethostname())
org = data['org']
region = data['region']
city = data['city']

get_system_info = {
    "os_name": os_name,
    "system_uuid": system_uuid,
    'public_ip': public_ip,
    "mac_address": mac_address,
    'ip_address': ip_add,
    'org': org,
    'region': region,
    'city': city
}

class CceApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel = tk.Tk() if master is None else tk.Toplevel(master)

        self.logoText = ttk.Label(self.toplevel)
        self.img_ClointLOGONew2 = tk.PhotoImage(file=name_logo_path)
        self.img_ClointLOGONew2 = self.img_ClointLOGONew2.subsample(5, 5)
        self.logoText.configure(
            anchor='center', background='#000000', borderwidth='20', compound='top')
        self.logoText.configure(
            font='{Calibri} 20 {bold}', foreground='#ff8000', image=self.img_ClointLOGONew2, takefocus=True) # problem line
        self.logoText.configure(text='Community Edition')
        self.logoText.grid(column='0', sticky='n')
        self.toplevel.columnconfigure('0', pad='0')

        email = ""
        if os.path.exists(data_path):
            with open(data_path, 'r') as file:
                data = json.load(file)
            email = data['email']
        else:
            data = dict()
            data['name'] = ''
            data['email'] = ''
            data['verified'] = False
            data['env_var_set'] = False
            data['scripts_path_added'] = False
            data['device_registered'] = False
            with open(data_path, 'w') as file:
                json.dump(data, file)

        self.email = tk.StringVar(value=email)
        if self.email.get() == '':

            self.emailFeild = tk.Entry(self.toplevel)
            self.emailFeild.configure(
                background='#ffffff', borderwidth='2', font='{Calibri} 14 {}', foreground='#0000ff')
            self.emailFeild.configure(
                justify='center', relief='flat', selectborderwidth='0', takefocus=False)
            self.emailFeild.configure(textvariable=self.email, width='60')
            _text_ = '''Paste the token here'''
            self.emailFeild.delete('0', 'end')
            self.emailFeild.insert('0', _text_)
            self.emailFeild.grid(column='0', ipady='3',
                                 padx='0', pady='20', row='1')
            self.toplevel.rowconfigure(
                '1', minsize='0', pad='0', uniform='None')

            def click(event):
                self.emailFeild.configure(state='normal')
                self.emailFeild.delete(0, 'end')
                self.emailFeild.unbind('<Button-1>', clicked)

            clicked = self.emailFeild.bind('<Button-1>', click)

            self.submitemail = tk.Button(self.toplevel)
            self.submitemail.configure(
                activebackground='#1a0900', activeforeground='#00ff00', background='#000000', font='{Calibri} 14 {bold}')
            self.submitemail.configure(foreground='#00ea00', text='Submit')
            self.submitemail.grid(column='1', ipadx='5',
                                  ipady='0', padx='0', pady='10', row='1')
            self.submitemail.configure(command=self.submit_email)
            
            self.skipemail = tk.Button(self.toplevel)
            self.skipemail.configure(
                activebackground='#1a0900', activeforeground='#00ff00', background='#000000', font='{Calibri} 14 {bold}')
            self.skipemail.configure(foreground='#00ea00', text='Skip')
            self.skipemail.grid(column='0', ipadx='5',
                                  ipady='0', padx='10', pady='10', row='2')
            self.skipemail.configure(command=self.quit)
        
        self.img_Splash = tk.PhotoImage(file=round_logo_path)
        self.toplevel.configure(background='#000000',
                                cursor='arrow', height='400', width='1200')
        self.toplevel.iconphoto(True, self.img_Splash)            # problem line
        self.toplevel.resizable(False, False)
        self.toplevel.title('ClointFusion Community Edition')

        # Main widget
        self.mainwindow = self.toplevel

    def run(self):
        self.mainwindow.mainloop()

    def start_selftest(self):
        pass

    def quit(self):
        self.mainwindow.quit()
        self.mainwindow.destroy()

    def submit_email(self):
        _email_ = self.email.get()

        if _email_.isspace() or _email_ == 'Paste the Token' or _email_ == "":
            return
        try:
            registerd, registered_data = register_device(_email_)
            if registerd:
                global user_email
                user_email = _email_
                with open(data_path, "r") as file:
                    data = json.load(file)

                data['email'] = registered_data['email']
                data['device_registered'] = True
                data['verified'] = True
                data['name'] = registered_data['full_name']

                with open(data_path, "w") as file:
                    json.dump(data, file)

                import tkinter.messagebox as tkMessageBox
                tkMessageBox.showinfo(
                    "Success", "Device Registered Successfully")
                self.quit()
            else:
                import tkinter.messagebox as tkMessageBox
                tkMessageBox.showinfo("Error", registered_data['error'])
        except Exception as e:
            print(e)
            return

def register_device(token):
    import requests
    resp = requests.post(f"{server_ip}/register-device/",
                         data={'token': str(token),
                               'device_id': str(get_system_info['system_uuid']),
                               'device_os': str(get_system_info['os_name']),
                               'device_public_ip_address': str(get_system_info['public_ip']),
                               'device_mac_address': str(get_system_info['mac_address']),
                               'device_ip_address': str(get_system_info['ip_address']),
                               'device_org': str(get_system_info['org']),
                               'device_region': str(get_system_info['region']),
                               'device_city': str(get_system_info['city']),
                               }
                         )

    if resp.status_code == 201:
        print("Device registered successfully")
        data = json.loads(resp.text)
        return True, data
    else:
        print("Device not registered")
        return False, json.loads(resp.text)

def verify_with_server():
    # imports section
    import requests
    import json
    import os

    resp = requests.post(f"{server_ip}/verify-device/",
                         data={
                             'device_id': str(get_system_info['system_uuid']),
                             'device_os': str(get_system_info['os_name']),
                             'device_public_ip_address': str(get_system_info['public_ip']),
                         }
                         )

    if resp.status_code == 200:
        data = json.loads(resp.text)
        return True, data

    if resp.status_code == 504:
        if os.path.exists(data_path):
            with open(data_path, 'r') as file:
                data = json.load(file)
        return True, data

    else:
        try:
            if os.path.exists(data_path):
                with open(data_path, 'r') as file:
                    data = json.load(file)
                    data['email'] = ''
                    data['name'] = ''
                    data['device_registered'] = False
                    data['verified'] = False
                    data['ask_register'] = True
                    with open(data_path, 'w') as file:
                            json.dump(data, file)
            else:
                data = dict()
                data['name'] = ''
                data['email'] = ''
                data['verified'] = False
                data['env_var_set'] = False
                data['scripts_path_added'] = False
                data['device_registered'] = False
                data['ask_register'] = True
                with open(data_path, 'w') as file:
                    json.dump(data, file)
            
            app = CceApp()
            app.run()
            data = dict()
            data['name'] = name
            data['email'] = user_email
            return True, data
        except:
            return False, "Error"
