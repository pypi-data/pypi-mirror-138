from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error, cf_icon_cdt_file_path
# Functions Represent in this file


if os_name == windows_os:

    # Windows OS - Python 3.7
    if python_version == python_37:

        def message_counter_down_timer(strMsg="Calling ClointFusion Function in (seconds)", start_value=5):

            # Description:
            """
            Function to show count-down timer. Default is 5 seconds.
            Ex: message_counter_down_timer()
            """

            # import section
            import PySimpleGUI as sg
            from clointfusion.check_system import cf_logo_file_path
            import time
            # Response section
            status = False
            data = None

            try:
                layout = [[sg.Text(strMsg, justification='c')], [sg.Text('', size=(10, 0), font=('Helvetica', 20), justification='c', key='text')],
                          [sg.Image(filename=str(cf_logo_file_path),
                                    size=(60, 60))],
                          [sg.Exit(button_color=('white', 'firebrick4'), key='Cancel')]]

                window = sg.Window('ClointFusion - Countdown Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                                   grab_anywhere=False, element_justification='c', element_padding=(0, 0), finalize=True, icon=cf_icon_cdt_file_path)

                current_value = start_value + 1

                while True:
                    event, _ = window.read(timeout=2)
                    current_value = current_value - 1
                    time.sleep(1)

                    if current_value == 0:
                        status = True
                        break

                    if event in (sg.WINDOW_CLOSED, 'Cancel'):
                        status = False
                        print("Action cancelled by user")
                        break

                    window['text'].update(value=current_value)

                window.close()

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = status
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_pop_up(strMsg="", delay=3):
            # Description:
            """
            Specified message will popup on the screen for a specified duration of time.

            Parameters:
                strMsg  (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            import PySimpleGUI as sg

            # Response section
            status = False
            data = None

            try:
                sg.popup(strMsg, title='ClointFusion', auto_close_duration=delay, auto_close=True,
                         keep_on_top=True, background_color="white", text_color="black")  # ,icon=cloint_ico_logo_base64)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(str(e))
            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_flash(msg="", delay=3):
            # Description:
            """
            specified msg will popup for a specified duration of time with OK button.

            Parameters:
                msg     (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            from clointfusion.clointfusion import key_hit_enter
            from threading import Timer
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                r = Timer(int(delay), key_hit_enter)
                r.start()
                pg.alert(text=msg, title='ClointFusion', button='OK')

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_toast(message, website_url="", file_folder_path=""):

            # Description:
            """
            Function for displaying Windows 10 Toast Notifications.
            Pass website URL OR file / folder path that needs to be opened when user clicks on the toast notification.
            """

            # import section
            from clointfusion.check_system import cf_icon_cdt_file_path
            import webbrowser
            import os
            # Response section
            status = False
            data = None

            try:
                if os_name == windows_os:
                    from win10toast_click import ToastNotifier
                    toaster = ToastNotifier()

                    if website_url:

                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open URL".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            callback_on_click=lambda: webbrowser.open_new(
                                website_url)  # click notification to run function
                        )

                    elif file_folder_path:
                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            # click notification to run function
                            callback_on_click=lambda: os.startfile(
                                file_folder_path)
                        )

                    else:
                        toaster.show_toast(
                            "ClointFusion",  # title
                            message,  # message
                            icon_path=cf_icon_cdt_file_path,  # 'icon_path'
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                        )
                else:
                    print("This function works only on Windows OS")

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]


# Windows OS - Python 3.8
    elif python_version == python_38:

        def message_counter_down_timer(strMsg="Calling ClointFusion Function in (seconds)", start_value=5):

            # Description:
            """
            Function to show count-down timer. Default is 5 seconds.
            Ex: message_counter_down_timer()
            """

            # import section
            import PySimpleGUI as sg
            from clointfusion.check_system import cf_logo_file_path
            import time
            # Response section
            status = False
            data = None

            try:
                layout = [[sg.Text(strMsg, justification='c')], [sg.Text('', size=(10, 0), font=('Helvetica', 20), justification='c', key='text')],
                          [sg.Image(filename=str(cf_logo_file_path),
                                    size=(60, 60))],
                          [sg.Exit(button_color=('white', 'firebrick4'), key='Cancel')]]

                window = sg.Window('ClointFusion - Countdown Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                                   grab_anywhere=False, element_justification='c', element_padding=(0, 0), finalize=True, icon=cf_icon_cdt_file_path)

                current_value = start_value + 1

                while True:
                    event, _ = window.read(timeout=2)
                    current_value = current_value - 1
                    time.sleep(1)

                    if current_value == 0:
                        status = True
                        break

                    if event in (sg.WINDOW_CLOSED, 'Cancel'):
                        status = False
                        print("Action cancelled by user")
                        break

                    window['text'].update(value=current_value)

                window.close()

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = status
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_pop_up(strMsg="", delay=3):
            # Description:
            """
            Specified message will popup on the screen for a specified duration of time.

            Parameters:
                strMsg  (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            import PySimpleGUI as sg

            # Response section
            status = False
            data = None

            try:
                sg.popup(strMsg, title='ClointFusion', auto_close_duration=delay, auto_close=True,
                         keep_on_top=True, background_color="white", text_color="black")  # ,icon=cloint_ico_logo_base64)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(str(e))
            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_flash(msg="", delay=3):
            # Description:
            """
            specified msg will popup for a specified duration of time with OK button.

            Parameters:
                msg     (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            from clointfusion.clointfusion import key_hit_enter
            from threading import Timer
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                r = Timer(int(delay), key_hit_enter)
                r.start()
                pg.alert(text=msg, title='ClointFusion', button='OK')

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_toast(message, website_url="", file_folder_path=""):

            # Description:
            """
            Function for displaying Windows 10 Toast Notifications.
            Pass website URL OR file / folder path that needs to be opened when user clicks on the toast notification.
            """

            # import section
            from clointfusion.check_system import cf_icon_cdt_file_path
            import webbrowser
            import os
            # Response section
            status = False
            data = None

            try:
                if os_name == windows_os:
                    from win10toast_click import ToastNotifier
                    toaster = ToastNotifier()

                    if website_url:

                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open URL".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            callback_on_click=lambda: webbrowser.open_new(
                                website_url)  # click notification to run function
                        )

                    elif file_folder_path:
                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            # click notification to run function
                            callback_on_click=lambda: os.startfile(
                                file_folder_path)
                        )

                    else:
                        toaster.show_toast(
                            "ClointFusion",  # title
                            message,  # message
                            icon_path=cf_icon_cdt_file_path,  # 'icon_path'
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                        )
                else:
                    print("This function works only on Windows OS")

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]


# Windows OS - Python 3.9
    elif python_version == python_39:

        def message_counter_down_timer(strMsg="Calling ClointFusion Function in (seconds)", start_value=5):

            # Description:
            """
            Function to show count-down timer. Default is 5 seconds.
            Ex: message_counter_down_timer()
            """

            # import section
            import PySimpleGUI as sg
            from clointfusion.check_system import cf_logo_file_path
            import time
            # Response section
            status = False
            data = None

            try:
                layout = [[sg.Text(strMsg, justification='c')], [sg.Text('', size=(10, 0), font=('Helvetica', 20), justification='c', key='text')],
                          [sg.Image(filename=str(cf_logo_file_path),
                                    size=(60, 60))],
                          [sg.Exit(button_color=('white', 'firebrick4'), key='Cancel')]]

                window = sg.Window('ClointFusion - Countdown Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                                   grab_anywhere=False, element_justification='c', element_padding=(0, 0), finalize=True, icon=cf_icon_cdt_file_path)

                current_value = start_value + 1

                while True:
                    event, _ = window.read(timeout=2)
                    current_value = current_value - 1
                    time.sleep(1)

                    if current_value == 0:
                        status = True
                        break

                    if event in (sg.WINDOW_CLOSED, 'Cancel'):
                        status = False
                        print("Action cancelled by user")
                        break

                    window['text'].update(value=current_value)

                window.close()

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = status
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_pop_up(strMsg="", delay=3):
            # Description:
            """
            Specified message will popup on the screen for a specified duration of time.

            Parameters:
                strMsg  (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            import PySimpleGUI as sg

            # Response section
            status = False
            data = None

            try:
                sg.popup(strMsg, title='ClointFusion', auto_close_duration=delay, auto_close=True,
                         keep_on_top=True, background_color="white", text_color="black")  # ,icon=cloint_ico_logo_base64)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(str(e))
            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_flash(msg="", delay=3):
            # Description:
            """
            specified msg will popup for a specified duration of time with OK button.

            Parameters:
                msg     (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            from clointfusion.clointfusion import key_hit_enter
            from threading import Timer
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                r = Timer(int(delay), key_hit_enter)
                r.start()
                pg.alert(text=msg, title='ClointFusion', button='OK')

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_toast(message, website_url="", file_folder_path=""):

            # Description:
            """
            Function for displaying Windows 10 Toast Notifications.
            Pass website URL OR file / folder path that needs to be opened when user clicks on the toast notification.
            """

            # import section
            from clointfusion.check_system import cf_icon_cdt_file_path
            import webbrowser
            import os
            # Response section
            status = False
            data = None

            try:
                if os_name == windows_os:
                    from win10toast_click import ToastNotifier
                    toaster = ToastNotifier()

                    if website_url:

                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open URL".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            callback_on_click=lambda: webbrowser.open_new(
                                website_url)  # click notification to run function
                        )

                    elif file_folder_path:
                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            # click notification to run function
                            callback_on_click=lambda: os.startfile(
                                file_folder_path)
                        )

                    else:
                        toaster.show_toast(
                            "ClointFusion",  # title
                            message,  # message
                            icon_path=cf_icon_cdt_file_path,  # 'icon_path'
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                        )
                else:
                    print("This function works only on Windows OS")

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]


# Windows OS - Python 3.10
    elif python_version == python_310:

        def message_counter_down_timer(strMsg="Calling ClointFusion Function in (seconds)", start_value=5):

            # Description:
            """
            Function to show count-down timer. Default is 5 seconds.
            Ex: message_counter_down_timer()
            """

            # import section
            import PySimpleGUI as sg
            from clointfusion.check_system import cf_logo_file_path
            import time
            # Response section
            status = False
            data = None

            try:
                layout = [[sg.Text(strMsg, justification='c')], [sg.Text('', size=(10, 0), font=('Helvetica', 20), justification='c', key='text')],
                          [sg.Image(filename=str(cf_logo_file_path),
                                    size=(60, 60))],
                          [sg.Exit(button_color=('white', 'firebrick4'), key='Cancel')]]

                window = sg.Window('ClointFusion - Countdown Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                                   grab_anywhere=False, element_justification='c', element_padding=(0, 0), finalize=True, icon=cf_icon_cdt_file_path)

                current_value = start_value + 1

                while True:
                    event, _ = window.read(timeout=2)
                    current_value = current_value - 1
                    time.sleep(1)

                    if current_value == 0:
                        status = True
                        break

                    if event in (sg.WINDOW_CLOSED, 'Cancel'):
                        status = False
                        print("Action cancelled by user")
                        break

                    window['text'].update(value=current_value)

                window.close()

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = status
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_pop_up(strMsg="", delay=3):
            # Description:
            """
            Specified message will popup on the screen for a specified duration of time.

            Parameters:
                strMsg  (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            import PySimpleGUI as sg

            # Response section
            status = False
            data = None

            try:
                sg.popup(strMsg, title='ClointFusion', auto_close_duration=delay, auto_close=True,
                         keep_on_top=True, background_color="white", text_color="black")  # ,icon=cloint_ico_logo_base64)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(str(e))
            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_flash(msg="", delay=3):
            # Description:
            """
            specified msg will popup for a specified duration of time with OK button.

            Parameters:
                msg     (str) : message to popup.
                delay   (int) : duration of the popup.
            """

            # import section
            from clointfusion.clointfusion import key_hit_enter
            from threading import Timer
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                r = Timer(int(delay), key_hit_enter)
                r.start()
                pg.alert(text=msg, title='ClointFusion', button='OK')

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

        def message_toast(message, website_url="", file_folder_path=""):

            # Description:
            """
            Function for displaying Windows 10 Toast Notifications.
            Pass website URL OR file / folder path that needs to be opened when user clicks on the toast notification.
            """

            # import section
            from clointfusion.check_system import cf_icon_cdt_file_path
            import webbrowser
            import os
            # Response section
            status = False
            data = None

            try:
                if os_name == windows_os:
                    from win10toast_click import ToastNotifier
                    toaster = ToastNotifier()

                    if website_url:

                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open URL".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            callback_on_click=lambda: webbrowser.open_new(
                                website_url)  # click notification to run function
                        )

                    elif file_folder_path:
                        toaster.show_toast(
                            "ClointFusion",
                            "{}. Click to open".format(message),
                            icon_path=cf_icon_cdt_file_path,
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                            # click notification to run function
                            callback_on_click=lambda: os.startfile(
                                file_folder_path)
                        )

                    else:
                        toaster.show_toast(
                            "ClointFusion",  # title
                            message,  # message
                            icon_path=cf_icon_cdt_file_path,  # 'icon_path'
                            duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
                            threaded=True,  # True = run other code in parallel; False = code execution will wait till notification disappears
                        )
                else:
                    print("This function works only on Windows OS")

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status == True and data != None:
                    return [status, data]
                return [status]

    else:
        raise Exception("Python version not supported")


elif os_name == linux_os:

    # Ubuntu OS - Python 3.7
    if python_version == python_37:
        pass


# Ubuntu OS - Python 3.8
    elif python_version == python_38:
        pass


# Ubuntu OS - Python 3.9
    elif python_version == python_39:
        pass


# Ubuntu OS - Python 3.10
    elif python_version == python_310:
        pass

    else:
        raise Exception("Python version not supported")


elif os_name == mac_os:

    # Mac OS - Python 3.7
    if python_version == python_37:
        pass


# Mac OS - Python 3.8
    elif python_version == python_38:
        pass


# Mac OS - Python 3.9
    elif python_version == python_39:
        pass


# Mac OS - Python 3.10
    elif python_version == python_310:
        pass

    else:
        raise Exception("Python version not supported")
