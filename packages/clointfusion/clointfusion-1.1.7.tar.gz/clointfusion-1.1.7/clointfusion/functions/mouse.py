from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error
# Functions Represent in this file


if os_name == windows_os:

    # Windows OS - Python 3.7
    if python_version == python_37:

        def mouse_click(x='', y='', left_or_right="left", no_of_clicks=1):

            # Description:
            """
            Clicks at the given X Y Co-ordinates on the screen using single / double / triple click(s). Default clicks on current position.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                left_or_right (str, optional): Which mouse button.
                Eg: right or left, Defaults: left.
                no_of_click (int, optional): Number of times specified mouse button to be clicked.
                Eg: 1 or 2, Max 3. Defaults: 1.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if not x or not y:
                    x, y = pg.position()

                time.sleep(1)

                if x and y:
                    x, y = int(x), int(y)
                    no_of_clicks = 3 if no_of_clicks > 3 else no_of_clicks
                    pg.click(x, y, clicks=no_of_clicks, button=left_or_right)
                    time.sleep(1)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_move(x="", y=""):

            # Description:
            """
            Moves the cursor to the given X Y Co-ordinates.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                
                if x and y:
                    x, y = int(x), int(y)
                    time.sleep(0.2)
                    pg.moveTo(x, y)
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_drag_from_to(x1="", y1="", x2="", y2="", delay=0.5):

            # Description:
            """
            Clicks and drags from x1 y1 co-ordinates to x2 y2 Co-ordinates on the screen

            Args:
                x1 or x2 (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y1 or y2 (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                delay (float, optional): Seconds to wait while performing action. 
                Eg: 1 or 0.5, Defaults to 0.5.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if x1 and y1 and x2 and y2:
                    time.sleep(0.2)
                    x1, y1 = int(x1), int(y1)
                    x2, y2 = int(x2), int(y2)
                    pg.moveTo(x1, y1, duration=delay)
                    pg.dragTo(x2, y2, duration=delay, button='left')
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")
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

        def mouse_search_snip_return_coordinates_x_y(img="", wait=180):

            # Description:
            """
            Searches the given image on the screen and returns its center of X Y co-ordinates.

            Args:
                img (str, optional): Path of the image. 
                Eg: D:\Files\Image.png, Defaults to "".
                wait (int, optional): Time you want to wait while program searches for image repeatably.
                Eg: 10 or 100 Defaults to 180.

            Returns:
                bool: If function is failed returns False.
                tuple (x, y): Image Center co-ordinates.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                region = (0, 0, pg.size()[0], pg.size()[1])
                if not img:
                    raise Exception("Image path is required.")

                time.sleep(1)

                pos = pg.locateOnScreen(img, region=region)
                i = 0
                while pos == None and i < int(wait):
                    pos = ()
                    pos = pg.locateOnScreen(img, region=region)
                    time.sleep(1)
                    i = i + 1

                time.sleep(1)

                if pos:
                    x, y = pos.left + \
                        int(pos.width / 2), pos.top + int(pos.height / 2)
                    data = (x, y)

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

        def mouse_click(x='', y='', left_or_right="left", no_of_clicks=1):

            # Description:
            """
            Clicks at the given X Y Co-ordinates on the screen using single / double / triple click(s). Default clicks on current position.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                left_or_right (str, optional): Which mouse button.
                Eg: right or left, Defaults: left.
                no_of_click (int, optional): Number of times specified mouse button to be clicked.
                Eg: 1 or 2, Max 3. Defaults: 1.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if not x or not y:
                    x, y = pg.position()

                time.sleep(1)

                if x and y:
                    x, y = int(x), int(y)
                    no_of_clicks = 3 if no_of_clicks > 3 else no_of_clicks
                    pg.click(x, y, clicks=no_of_clicks, button=left_or_right)
                    time.sleep(1)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_move(x="", y=""):

            # Description:
            """
            Moves the cursor to the given X Y Co-ordinates.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                
                if x and y:
                    x, y = int(x), int(y)
                    time.sleep(0.2)
                    pg.moveTo(x, y)
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_drag_from_to(x1="", y1="", x2="", y2="", delay=0.5):

            # Description:
            """
            Clicks and drags from x1 y1 co-ordinates to x2 y2 Co-ordinates on the screen

            Args:
                x1 or x2 (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y1 or y2 (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                delay (float, optional): Seconds to wait while performing action. 
                Eg: 1 or 0.5, Defaults to 0.5.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if x1 and y1 and x2 and y2:
                    time.sleep(0.2)
                    x1, y1 = int(x1), int(y1)
                    x2, y2 = int(x2), int(y2)
                    pg.moveTo(x1, y1, duration=delay)
                    pg.dragTo(x2, y2, duration=delay, button='left')
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")
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

        def mouse_search_snip_return_coordinates_x_y(img="", wait=180):

            # Description:
            """
            Searches the given image on the screen and returns its center of X Y co-ordinates.

            Args:
                img (str, optional): Path of the image. 
                Eg: D:\Files\Image.png, Defaults to "".
                wait (int, optional): Time you want to wait while program searches for image repeatably.
                Eg: 10 or 100 Defaults to 180.

            Returns:
                bool: If function is failed returns False.
                tuple (x, y): Image Center co-ordinates.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                region = (0, 0, pg.size()[0], pg.size()[1])
                if not img:
                    raise Exception("Image path is required.")

                time.sleep(1)

                pos = pg.locateOnScreen(img, region=region)
                i = 0
                while pos == None and i < int(wait):
                    pos = ()
                    pos = pg.locateOnScreen(img, region=region)
                    time.sleep(1)
                    i = i + 1

                time.sleep(1)

                if pos:
                    x, y = pos.left + \
                        int(pos.width / 2), pos.top + int(pos.height / 2)
                    status = (x, y)

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

        def mouse_click(x='', y='', left_or_right="left", no_of_clicks=1):

            # Description:
            """
            Clicks at the given X Y Co-ordinates on the screen using single / double / triple click(s). Default clicks on current position.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                left_or_right (str, optional): Which mouse button.
                Eg: right or left, Defaults: left.
                no_of_click (int, optional): Number of times specified mouse button to be clicked.
                Eg: 1 or 2, Max 3. Defaults: 1.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if not x or not y:
                    x, y = pg.position()

                time.sleep(1)

                if x and y:
                    x, y = int(x), int(y)
                    no_of_clicks = 3 if no_of_clicks > 3 else no_of_clicks
                    pg.click(x, y, clicks=no_of_clicks, button=left_or_right)
                    time.sleep(1)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_move(x="", y=""):

            # Description:
            """
            Moves the cursor to the given X Y Co-ordinates.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                
                if x and y:
                    x, y = int(x), int(y)
                    time.sleep(0.2)
                    pg.moveTo(x, y)
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_drag_from_to(x1="", y1="", x2="", y2="", delay=0.5):

            # Description:
            """
            Clicks and drags from x1 y1 co-ordinates to x2 y2 Co-ordinates on the screen

            Args:
                x1 or x2 (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y1 or y2 (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                delay (float, optional): Seconds to wait while performing action. 
                Eg: 1 or 0.5, Defaults to 0.5.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if x1 and y1 and x2 and y2:
                    time.sleep(0.2)
                    x1, y1 = int(x1), int(y1)
                    x2, y2 = int(x2), int(y2)
                    pg.moveTo(x1, y1, duration=delay)
                    pg.dragTo(x2, y2, duration=delay, button='left')
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")
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

        def mouse_search_snip_return_coordinates_x_y(img="", wait=180):

            # Description:
            """
            Searches the given image on the screen and returns its center of X Y co-ordinates.

            Args:
                img (str, optional): Path of the image. 
                Eg: D:\Files\Image.png, Defaults to "".
                wait (int, optional): Time you want to wait while program searches for image repeatably.
                Eg: 10 or 100 Defaults to 180.

            Returns:
                bool: If function is failed returns False.
                tuple (x, y): Image Center co-ordinates.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                region = (0, 0, pg.size()[0], pg.size()[1])
                if not img:
                    raise Exception("Image path is required.")

                time.sleep(1)

                pos = pg.locateOnScreen(img, region=region)
                i = 0
                while pos == None and i < int(wait):
                    pos = ()
                    pos = pg.locateOnScreen(img, region=region)
                    time.sleep(1)
                    i = i + 1

                time.sleep(1)

                if pos:
                    x, y = pos.left + \
                        int(pos.width / 2), pos.top + int(pos.height / 2)
                    status = (x, y)

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

        def mouse_click(x='', y='', left_or_right="left", no_of_clicks=1):

            # Description:
            """
            Clicks at the given X Y Co-ordinates on the screen using single / double / triple click(s). Default clicks on current position.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                left_or_right (str, optional): Which mouse button.
                Eg: right or left, Defaults: left.
                no_of_click (int, optional): Number of times specified mouse button to be clicked.
                Eg: 1 or 2, Max 3. Defaults: 1.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if not x or not y:
                    x, y = pg.position()

                time.sleep(1)

                if x and y:
                    x, y = int(x), int(y)
                    no_of_clicks = 3 if no_of_clicks > 3 else no_of_clicks
                    pg.click(x, y, clicks=no_of_clicks, button=left_or_right)
                    time.sleep(1)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_move(x="", y=""):

            # Description:
            """
            Moves the cursor to the given X Y Co-ordinates.

            Args:
                x (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                
                if x and y:
                    x, y = int(x), int(y)
                    time.sleep(0.2)
                    pg.moveTo(x, y)
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")

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

        def mouse_drag_from_to(x1="", y1="", x2="", y2="", delay=0.5):

            # Description:
            """
            Clicks and drags from x1 y1 co-ordinates to x2 y2 Co-ordinates on the screen

            Args:
                x1 or x2 (int): x-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                y1 or y2 (int): y-coordinate on screen.
                Eg: 369 or 435, Defaults: ''.
                delay (float, optional): Seconds to wait while performing action. 
                Eg: 1 or 0.5, Defaults to 0.5.

            Returns:
                bool: Whether the function is successful or failed.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                if x1 and y1 and x2 and y2:
                    time.sleep(0.2)
                    x1, y1 = int(x1), int(y1)
                    x2, y2 = int(x2), int(y2)
                    pg.moveTo(x1, y1, duration=delay)
                    pg.dragTo(x2, y2, duration=delay, button='left')
                    time.sleep(0.2)
                else:
                    raise Exception("X and Y co-ordinates are required.")
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

        def mouse_search_snip_return_coordinates_x_y(img="", wait=180):

            # Description:
            """
            Searches the given image on the screen and returns its center of X Y co-ordinates.

            Args:
                img (str, optional): Path of the image. 
                Eg: D:\Files\Image.png, Defaults to "".
                wait (int, optional): Time you want to wait while program searches for image repeatably.
                Eg: 10 or 100 Defaults to 180.

            Returns:
                bool: If function is failed returns False.
                tuple (x, y): Image Center co-ordinates.
            """

            # import section
            import time
            import pyautogui as pg

            # Response section
            status = False
            data = None

            try:
                region = (0, 0, pg.size()[0], pg.size()[1])
                if not img:
                    raise Exception("Image path is required.")

                time.sleep(1)

                pos = pg.locateOnScreen(img, region=region)
                i = 0
                while pos == None and i < int(wait):
                    pos = ()
                    pos = pg.locateOnScreen(img, region=region)
                    time.sleep(1)
                    i = i + 1

                time.sleep(1)

                if pos:
                    x, y = pos.left + \
                        int(pos.width / 2), pos.top + int(pos.height / 2)
                    status = (x, y)

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
