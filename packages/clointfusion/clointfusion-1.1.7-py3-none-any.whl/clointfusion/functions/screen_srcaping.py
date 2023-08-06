from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error

# Functions Represent in this file


if os_name == windows_os:

    # Windows OS - Python 3.7
    if python_version == python_37:

        def scrape_save_contents_to_notepad(folderPathToSaveTheNotepad="", switch_to_window="", X=0, Y=0):

            # Description:
            """
            Copy pastes all the available text on the screen to notepad and saves it.
            """

            # import section
            from clointfusion.clointfusion import message_counter_down_timer, window_activate_and_maximize_windows, mouse_click
            import time
            import pyautogui as pg
            import pathlib as Path
            import clipboard

            # Response section
            status = False
            data = None

            try:

                if not folderPathToSaveTheNotepad:
                    raise Exception("Folder path to save the notepad is not provided.")

                message_counter_down_timer("Screen scraping in (seconds)", 3)

                if switch_to_window:
                    if os_name == windows_os:
                        window_activate_and_maximize_windows(switch_to_window)
                    elif os_name == linux_os:
                        mouse_click(100, 100)

                time.sleep(1)
                if X == 0 and Y == 0:
                    X = pg.size()[0]/2
                    Y = pg.size()[1]/2
                pg.click(X, Y)
                time.sleep(0.5)

                pg.hotkey("ctrl", "a")
                time.sleep(1)

                pg.hotkey("ctrl", "c")
                time.sleep(1)

                clipboard_data = clipboard.paste()
                time.sleep(2)

                screen_clear_search()

                notepad_file_path = Path(folderPathToSaveTheNotepad)
                notepad_file_path = notepad_file_path / 'notepad-contents.txt'

                f = open(notepad_file_path, "w", encoding="utf-8")
                f.write(clipboard_data)
                time.sleep(10)
                f.close()

                clipboard_data = ''
                data = str(notepad_file_path)

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

        def screen_clear_search(delay=0.2):

            # Description:
            """
            Clears previously found text (crtl+f highlight)
            """

            # import section
            # from clointfusion.clointfusion import text_to_speech
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite("^%#")
                time.sleep(delay)
                pg.hotkey("esc")
                time.sleep(delay)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def search_highlight_tab_enter_open(searchText="", hitEnterKey="Yes", shift_tab='No'):

            # Description:
            """
            Searches for a text on screen using crtl+f and hits enter.
            This function is useful in Citrix environment
            """

            # import section
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(0.5)

                pg.hotkey("ctrl", "f")
                time.sleep(0.5)

                pg.write(searchText)
                time.sleep(0.5)

                pg.hotkey("enter")
                time.sleep(0.5)

                pg.hotkey("esc")
                time.sleep(0.2)
                if hitEnterKey.lower() == "yes" and shift_tab.lower() == "yes":

                    pg.hotkey("tab")
                    time.sleep(0.3)

                    pg.hotkey("shift", "tab")
                    time.sleep(0.3)

                    pg.hotkey("enter")
                    time.sleep(2)
                elif hitEnterKey.lower() == "yes" and shift_tab.lower() == "no":

                    pg.hotkey("enter")
                    time.sleep(2)

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

        def find_text_on_screen(searchText="", delay=0.1, occurance=1, isSearchToBeCleared=False):

            # Description:
            """
            Clears previous search and finds the provided text on screen.
            """

            # import section
            import time
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                screen_clear_search()  # default

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(delay)
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite(searchText)
                time.sleep(delay)

                for i in range(occurance-1):
                    pg.hotkey("enter")
                    time.sleep(delay)

                pg.hotkey("esc")
                time.sleep(delay)

                if isSearchToBeCleared:
                    screen_clear_search()

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

        def scrape_save_contents_to_notepad(folderPathToSaveTheNotepad="", switch_to_window="", X=0, Y=0):

            # Description:
            """
            Copy pastes all the available text on the screen to notepad and saves it.
            """

            # import section
            from clointfusion.clointfusion import message_counter_down_timer, window_activate_and_maximize_windows, mouse_click
            import time
            import pyautogui as pg
            import pathlib as Path
            import clipboard

            # Response section
            status = False
            data = None

            try:

                if not folderPathToSaveTheNotepad:
                    raise Exception("Folder path to save the notepad is not provided.")

                message_counter_down_timer("Screen scraping in (seconds)", 3)

                if switch_to_window:
                    if os_name == windows_os:
                        window_activate_and_maximize_windows(switch_to_window)
                    elif os_name == linux_os:
                        mouse_click(100, 100)

                time.sleep(1)
                if X == 0 and Y == 0:
                    X = pg.size()[0]/2
                    Y = pg.size()[1]/2
                pg.click(X, Y)
                time.sleep(0.5)

                pg.hotkey("ctrl", "a")
                time.sleep(1)

                pg.hotkey("ctrl", "c")
                time.sleep(1)

                clipboard_data = clipboard.paste()
                time.sleep(2)

                screen_clear_search()

                notepad_file_path = Path(folderPathToSaveTheNotepad)
                notepad_file_path = notepad_file_path / 'notepad-contents.txt'

                f = open(notepad_file_path, "w", encoding="utf-8")
                f.write(clipboard_data)
                time.sleep(10)
                f.close()

                clipboard_data = ''
                data = str(notepad_file_path)

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

        def screen_clear_search(delay=0.2):

            # Description:
            """
            Clears previously found text (crtl+f highlight)
            """

            # import section
            # from clointfusion.clointfusion import text_to_speech
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite("^%#")
                time.sleep(delay)
                pg.hotkey("esc")
                time.sleep(delay)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def search_highlight_tab_enter_open(searchText="", hitEnterKey="Yes", shift_tab='No'):

            # Description:
            """
            Searches for a text on screen using crtl+f and hits enter.
            This function is useful in Citrix environment
            """

            # import section
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(0.5)

                pg.hotkey("ctrl", "f")
                time.sleep(0.5)

                pg.write(searchText)
                time.sleep(0.5)

                pg.hotkey("enter")
                time.sleep(0.5)

                pg.hotkey("esc")
                time.sleep(0.2)
                if hitEnterKey.lower() == "yes" and shift_tab.lower() == "yes":

                    pg.hotkey("tab")
                    time.sleep(0.3)

                    pg.hotkey("shift", "tab")
                    time.sleep(0.3)

                    pg.hotkey("enter")
                    time.sleep(2)
                elif hitEnterKey.lower() == "yes" and shift_tab.lower() == "no":

                    pg.hotkey("enter")
                    time.sleep(2)

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

        def find_text_on_screen(searchText="", delay=0.1, occurance=1, isSearchToBeCleared=False):

            # Description:
            """
            Clears previous search and finds the provided text on screen.
            """

            # import section
            import time
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                screen_clear_search()  # default

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(delay)
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite(searchText)
                time.sleep(delay)

                for i in range(occurance-1):
                    pg.hotkey("enter")
                    time.sleep(delay)

                pg.hotkey("esc")
                time.sleep(delay)

                if isSearchToBeCleared:
                    screen_clear_search()

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

        def scrape_save_contents_to_notepad(folderPathToSaveTheNotepad="", switch_to_window="", X=0, Y=0):

            # Description:
            """
            Copy pastes all the available text on the screen to notepad and saves it.
            """

            # import section
            from clointfusion.clointfusion import message_counter_down_timer, window_activate_and_maximize_windows, mouse_click
            import time
            import pyautogui as pg
            import pathlib as Path
            import clipboard

            # Response section
            status = False
            data = None

            try:

                if not folderPathToSaveTheNotepad:
                    raise Exception("Folder path to save the notepad is not provided.")

                message_counter_down_timer("Screen scraping in (seconds)", 3)

                if switch_to_window:
                    if os_name == windows_os:
                        window_activate_and_maximize_windows(switch_to_window)
                    elif os_name == linux_os:
                        mouse_click(100, 100)

                time.sleep(1)
                if X == 0 and Y == 0:
                    X = pg.size()[0]/2
                    Y = pg.size()[1]/2
                pg.click(X, Y)
                time.sleep(0.5)

                pg.hotkey("ctrl", "a")
                time.sleep(1)

                pg.hotkey("ctrl", "c")
                time.sleep(1)

                clipboard_data = clipboard.paste()
                time.sleep(2)

                screen_clear_search()

                notepad_file_path = Path(folderPathToSaveTheNotepad)
                notepad_file_path = notepad_file_path / 'notepad-contents.txt'

                f = open(notepad_file_path, "w", encoding="utf-8")
                f.write(clipboard_data)
                time.sleep(10)
                f.close()

                clipboard_data = ''
                data = str(notepad_file_path)

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

        def screen_clear_search(delay=0.2):

            # Description:
            """
            Clears previously found text (crtl+f highlight)
            """

            # import section
            # from clointfusion.clointfusion import text_to_speech
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite("^%#")
                time.sleep(delay)
                pg.hotkey("esc")
                time.sleep(delay)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def search_highlight_tab_enter_open(searchText="", hitEnterKey="Yes", shift_tab='No'):

            # Description:
            """
            Searches for a text on screen using crtl+f and hits enter.
            This function is useful in Citrix environment
            """

            # import section
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(0.5)

                pg.hotkey("ctrl", "f")
                time.sleep(0.5)

                pg.write(searchText)
                time.sleep(0.5)

                pg.hotkey("enter")
                time.sleep(0.5)

                pg.hotkey("esc")
                time.sleep(0.2)
                if hitEnterKey.lower() == "yes" and shift_tab.lower() == "yes":

                    pg.hotkey("tab")
                    time.sleep(0.3)

                    pg.hotkey("shift", "tab")
                    time.sleep(0.3)

                    pg.hotkey("enter")
                    time.sleep(2)
                elif hitEnterKey.lower() == "yes" and shift_tab.lower() == "no":

                    pg.hotkey("enter")
                    time.sleep(2)

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

        def find_text_on_screen(searchText="", delay=0.1, occurance=1, isSearchToBeCleared=False):

            # Description:
            """
            Clears previous search and finds the provided text on screen.
            """

            # import section
            import time
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                screen_clear_search()  # default

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(delay)
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite(searchText)
                time.sleep(delay)

                for i in range(occurance-1):
                    pg.hotkey("enter")
                    time.sleep(delay)

                pg.hotkey("esc")
                time.sleep(delay)

                if isSearchToBeCleared:
                    screen_clear_search()

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

        def scrape_save_contents_to_notepad(folderPathToSaveTheNotepad="", switch_to_window="", X=0, Y=0):

            # Description:
            """
            Copy pastes all the available text on the screen to notepad and saves it.
            """

            # import section
            from clointfusion.clointfusion import message_counter_down_timer, window_activate_and_maximize_windows, mouse_click
            import time
            import pyautogui as pg
            import pathlib as Path
            import clipboard

            # Response section
            status = False
            data = None

            try:

                if not folderPathToSaveTheNotepad:
                    raise Exception("Folder path to save the notepad is not provided.")

                message_counter_down_timer("Screen scraping in (seconds)", 3)

                if switch_to_window:
                    if os_name == windows_os:
                        window_activate_and_maximize_windows(switch_to_window)
                    elif os_name == linux_os:
                        mouse_click(100, 100)

                time.sleep(1)
                if X == 0 and Y == 0:
                    X = pg.size()[0]/2
                    Y = pg.size()[1]/2
                pg.click(X, Y)
                time.sleep(0.5)

                pg.hotkey("ctrl", "a")
                time.sleep(1)

                pg.hotkey("ctrl", "c")
                time.sleep(1)

                clipboard_data = clipboard.paste()
                time.sleep(2)

                screen_clear_search()

                notepad_file_path = Path(folderPathToSaveTheNotepad)
                notepad_file_path = notepad_file_path / 'notepad-contents.txt'

                f = open(notepad_file_path, "w", encoding="utf-8")
                f.write(clipboard_data)
                time.sleep(10)
                f.close()

                clipboard_data = ''
                data = str(notepad_file_path)

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

        def screen_clear_search(delay=0.2):

            # Description:
            """
            Clears previously found text (crtl+f highlight)
            """

            # import section
            # from clointfusion.clointfusion import text_to_speech
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite("^%#")
                time.sleep(delay)
                pg.hotkey("esc")
                time.sleep(delay)
            except Exception as e:
                report_error(e)

            else:
                status = True
            finally:
                if status is True and data is not None:
                    return [status, data]
                return [status]

        def search_highlight_tab_enter_open(searchText="", hitEnterKey="Yes", shift_tab='No'):

            # Description:
            """
            Searches for a text on screen using crtl+f and hits enter.
            This function is useful in Citrix environment
            """

            # import section
            import pyautogui as pg
            import time
            # Response section
            status = False
            data = None

            try:

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(0.5)

                pg.hotkey("ctrl", "f")
                time.sleep(0.5)

                pg.write(searchText)
                time.sleep(0.5)

                pg.hotkey("enter")
                time.sleep(0.5)

                pg.hotkey("esc")
                time.sleep(0.2)
                if hitEnterKey.lower() == "yes" and shift_tab.lower() == "yes":

                    pg.hotkey("tab")
                    time.sleep(0.3)

                    pg.hotkey("shift", "tab")
                    time.sleep(0.3)

                    pg.hotkey("enter")
                    time.sleep(2)
                elif hitEnterKey.lower() == "yes" and shift_tab.lower() == "no":

                    pg.hotkey("enter")
                    time.sleep(2)

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

        def find_text_on_screen(searchText="", delay=0.1, occurance=1, isSearchToBeCleared=False):

            # Description:
            """
            Clears previous search and finds the provided text on screen.
            """

            # import section
            import time
            import pyautogui as pg
            # Response section
            status = False
            data = None

            try:
                screen_clear_search()  # default

                if not searchText:
                    raise Exception("Search text is not provided.")

                time.sleep(delay)
                pg.hotkey("ctrl", "f")
                time.sleep(delay)
                pg.typewrite(searchText)
                time.sleep(delay)

                for i in range(occurance-1):
                    pg.hotkey("enter")
                    time.sleep(delay)

                pg.hotkey("esc")
                time.sleep(delay)

                if isSearchToBeCleared:
                    screen_clear_search()

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
