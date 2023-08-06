from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error

# # Functions Represent in this file
#  - key_press
#  - key_write_enter
#  - key_hit_enter


if os_name == windows_os:

    # Windows OS - Python 3.7
    if python_version == python_37:

        def key_press(key_1='', key_2='', key_3='', write_to_window=""):

            # Description:
            """
            Emulates the given keystrokes.

            Args:
                key_1 (str, optional): Enter the 1st key
                Eg: ctrl or shift. Defaults to ''.
                key_2 (str, optional): Enter the 2nd key in combination.
                Eg: alt or A. Defaults to ''.
                key_3 (str, optional): Enter the 3rd key in combination.
                Eg: del or tab. Defaults to ''.
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate. Defaults to "".

            Supported Keys:
                ['\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',')', '*', '+', ',', '-', '.', '/',
                '0', '1', '2', '3', '4', '5', '6', '7','8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                'command', 'option', 'optionleft', 'optionright']

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if key_1 == '':
                    raise Exception("Key 1 is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                pg.hotkey(key_1, key_2, key_3)
                time.sleep(0.5)
                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except pg.FailSafeException:
                report_error(pg.FailSafeException)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_write_enter(text_to_write="", write_to_window="", delay_after_typing=1, key="e"):

            # Description:
            """
            Writes/Types the given text.

            Args:
                text_to_write (str, optional): Text you wanted to type
                Eg: ClointFusion is awesone. Defaults to "".
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate
                Eg: Notepad. Defaults to "".
                delay_after_typing (int, optional): Seconds in time to wait after entering the text
                Eg: 5. Defaults to 1.
                key (str, optional): Press Enter key after typing.
                Eg: t for tab. Defaults to e

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if not text_to_write:
                    raise Exception("Text to write is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())

                time.sleep(0.2)
                pg.write(text_to_write)
                if key.lower() == "e":
                    pg.hotkey("enter")
                if key.lower() == "t":
                    pg.hotkey("tab")
                time.sleep(delay_after_typing)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_hit_enter(write_to_window=""):

            # Description:
            """
            Enter key will be pressed once.

            Args:
                write_to_window (str, optional): (Only in Windows)Name of Window you want to activate.
                Eg: Notepad. Defaults to "".

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section

            try:
                window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                key_press(key_1="enter", write_to_window=write_to_window)
                time.sleep(0.5)
                status = True

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]


# Windows OS - Python 3.8
    elif python_version == python_38:

        def key_press(key_1='', key_2='', key_3='', write_to_window=""):

            # Description:
            """
            Emulates the given keystrokes.

            Args:
                key_1 (str, optional): Enter the 1st key
                Eg: ctrl or shift. Defaults to ''.
                key_2 (str, optional): Enter the 2nd key in combination.
                Eg: alt or A. Defaults to ''.
                key_3 (str, optional): Enter the 3rd key in combination.
                Eg: del or tab. Defaults to ''.
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate. Defaults to "".

            Supported Keys:
                ['\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',')', '*', '+', ',', '-', '.', '/',
                '0', '1', '2', '3', '4', '5', '6', '7','8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                'command', 'option', 'optionleft', 'optionright']

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if key_1 == '':
                    raise Exception("Key 1 is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                pg.hotkey(key_1, key_2, key_3)
                time.sleep(0.5)
                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except pg.FailSafeException:
                report_error(pg.FailSafeException)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_write_enter(text_to_write="", write_to_window="", delay_after_typing=1, key="e"):

            # Description:
            """
            Writes/Types the given text.

            Args:
                text_to_write (str, optional): Text you wanted to type
                Eg: ClointFusion is awesone. Defaults to "".
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate
                Eg: Notepad. Defaults to "".
                delay_after_typing (int, optional): Seconds in time to wait after entering the text
                Eg: 5. Defaults to 1.
                key (str, optional): Press Enter key after typing.
                Eg: t for tab. Defaults to e

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if not text_to_write:
                    raise Exception("Text to write is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())

                time.sleep(0.2)
                pg.write(text_to_write)
                if key.lower() == "e":
                    pg.hotkey("enter")
                if key.lower() == "t":
                    pg.hotkey("tab")
                time.sleep(delay_after_typing)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_hit_enter(write_to_window=""):

            # Description:
            """
            Enter key will be pressed once.

            Args:
                write_to_window (str, optional): (Only in Windows)Name of Window you want to activate.
                Eg: Notepad. Defaults to "".

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section

            try:
                window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                key_press(key_1="enter", write_to_window=write_to_window)
                time.sleep(0.5)
                status = True

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]


# Windows OS - Python 3.9
    elif python_version == python_39:

        def key_press(key_1='', key_2='', key_3='', write_to_window=""):

            # Description:
            """
            Emulates the given keystrokes.

            Args:
                key_1 (str, optional): Enter the 1st key
                Eg: ctrl or shift. Defaults to ''.
                key_2 (str, optional): Enter the 2nd key in combination.
                Eg: alt or A. Defaults to ''.
                key_3 (str, optional): Enter the 3rd key in combination.
                Eg: del or tab. Defaults to ''.
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate. Defaults to "".

            Supported Keys:
                ['\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',')', '*', '+', ',', '-', '.', '/',
                '0', '1', '2', '3', '4', '5', '6', '7','8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                'command', 'option', 'optionleft', 'optionright']

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if key_1 == '':
                    raise Exception("Key 1 is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                pg.hotkey(key_1, key_2, key_3)
                time.sleep(0.5)
                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except pg.FailSafeException:
                report_error(pg.FailSafeException)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_write_enter(text_to_write="", write_to_window="", delay_after_typing=1, key="e"):

            # Description:
            """
            Writes/Types the given text.

            Args:
                text_to_write (str, optional): Text you wanted to type
                Eg: ClointFusion is awesone. Defaults to "".
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate
                Eg: Notepad. Defaults to "".
                delay_after_typing (int, optional): Seconds in time to wait after entering the text
                Eg: 5. Defaults to 1.
                key (str, optional): Press Enter key after typing.
                Eg: t for tab. Defaults to e

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if not text_to_write:
                    raise Exception("Text to write is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())

                time.sleep(0.2)
                pg.write(text_to_write)
                if key.lower() == "e":
                    pg.hotkey("enter")
                if key.lower() == "t":
                    pg.hotkey("tab")
                time.sleep(delay_after_typing)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_hit_enter(write_to_window=""):

            # Description:
            """
            Enter key will be pressed once.

            Args:
                write_to_window (str, optional): (Only in Windows)Name of Window you want to activate.
                Eg: Notepad. Defaults to "".

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section

            try:
                window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                key_press(key_1="enter", write_to_window=write_to_window)
                time.sleep(0.5)
                status = True

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]


# Windows OS - Python 3.10
    elif python_version == python_310:

        def key_press(key_1='', key_2='', key_3='', write_to_window=""):

            # Description:
            """
            Emulates the given keystrokes.

            Args:
                key_1 (str, optional): Enter the 1st key
                Eg: ctrl or shift. Defaults to ''.
                key_2 (str, optional): Enter the 2nd key in combination.
                Eg: alt or A. Defaults to ''.
                key_3 (str, optional): Enter the 3rd key in combination.
                Eg: del or tab. Defaults to ''.
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate. Defaults to "".

            Supported Keys:
                ['\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',')', '*', '+', ',', '-', '.', '/',
                '0', '1', '2', '3', '4', '5', '6', '7','8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                'command', 'option', 'optionleft', 'optionright']

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if key_1 == '':
                    raise Exception("Key 1 is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                pg.hotkey(key_1, key_2, key_3)
                time.sleep(0.5)
                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except pg.FailSafeException:
                report_error(pg.FailSafeException)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_write_enter(text_to_write="", write_to_window="", delay_after_typing=1, key="e"):

            # Description:
            """
            Writes/Types the given text.

            Args:
                text_to_write (str, optional): Text you wanted to type
                Eg: ClointFusion is awesone. Defaults to "".
                write_to_window (str, optional): (Only in Windows) Name of Window you want to activate
                Eg: Notepad. Defaults to "".
                delay_after_typing (int, optional): Seconds in time to wait after entering the text
                Eg: 5. Defaults to 1.
                key (str, optional): Press Enter key after typing.
                Eg: t for tab. Defaults to e

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section
            try:
                if not text_to_write:
                    raise Exception("Text to write is empty.")

                if os_name == windows_os:
                    if write_to_window:
                        window_activate_and_maximize_windows(write_to_window)
                    window_activate_and_maximize_windows(window_get_active_window())

                time.sleep(0.2)
                pg.write(text_to_write)
                if key.lower() == "e":
                    pg.hotkey("enter")
                if key.lower() == "t":
                    pg.hotkey("tab")
                time.sleep(delay_after_typing)

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def key_hit_enter(write_to_window=""):

            # Description:
            """
            Enter key will be pressed once.

            Args:
                write_to_window (str, optional): (Only in Windows)Name of Window you want to activate.
                Eg: Notepad. Defaults to "".

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            from clointfusion.clointfusion import window_activate_and_maximize_windows, window_get_active_window

            # Response section
            status = False
            data = None

            # Logic section

            try:
                window_activate_and_maximize_windows(window_get_active_window())
                time.sleep(0.5)
                key_press(key_1="enter", write_to_window=write_to_window)
                time.sleep(0.5)
                status = True

                # If the function returns a value, it should be assigned to the data variable.
                # data = value
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
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
