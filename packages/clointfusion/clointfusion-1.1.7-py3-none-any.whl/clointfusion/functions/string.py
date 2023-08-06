from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error
# Functions Represent in this file


if os_name == windows_os:

    # Windows OS - Python 3.7
    if python_version == python_37:

        def string_extract_only_alphabets(inputString=""):

            # Description:
            """
            Returns only alphabets from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isalpha())

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

        def string_extract_only_numbers(inputString=""):
            # Description:
            """
            Returns only numbers from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isnumeric())

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

        def string_remove_special_characters(inputStr=""):

            # Description:
            """
            Removes all the special character.

            Parameters:
                inputStr  (str) : string for removing all the special character in it.

            Returns :
                outputStr (str) : returns the alphanumeric string.
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputStr:
                    raise Exception("Input String cannot be empty")

                if inputStr:
                    data = ''.join(e for e in inputStr if e.isalnum())

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

        def string_extract_only_alphabets(inputString=""):

            # Description:
            """
            Returns only alphabets from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isalpha())

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

        def string_extract_only_numbers(inputString=""):
            # Description:
            """
            Returns only numbers from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isnumeric())

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

        def string_remove_special_characters(inputStr=""):

            # Description:
            """
            Removes all the special character.

            Parameters:
                inputStr  (str) : string for removing all the special character in it.

            Returns :
                outputStr (str) : returns the alphanumeric string.
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputStr:
                    raise Exception("Input String cannot be empty")

                if inputStr:
                    data = ''.join(e for e in inputStr if e.isalnum())

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

        def string_extract_only_alphabets(inputString=""):

            # Description:
            """
            Returns only alphabets from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isalpha())

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

        def string_extract_only_numbers(inputString=""):
            # Description:
            """
            Returns only numbers from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isnumeric())

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

        def string_remove_special_characters(inputStr=""):

            # Description:
            """
            Removes all the special character.

            Parameters:
                inputStr  (str) : string for removing all the special character in it.

            Returns :
                outputStr (str) : returns the alphanumeric string.
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputStr:
                    raise Exception("Input String cannot be empty")

                if inputStr:
                    data = ''.join(e for e in inputStr if e.isalnum())

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

        def string_extract_only_alphabets(inputString=""):

            # Description:
            """
            Returns only alphabets from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isalpha())

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

        def string_extract_only_numbers(inputString=""):
            # Description:
            """
            Returns only numbers from given input string
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputString:
                    raise Exception("Input String cannot be empty")

                data = ''.join(e for e in inputString if e.isnumeric())

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

        def string_remove_special_characters(inputStr=""):

            # Description:
            """
            Removes all the special character.

            Parameters:
                inputStr  (str) : string for removing all the special character in it.

            Returns :
                outputStr (str) : returns the alphanumeric string.
            """

            # import section
            # Response section
            status = False
            data = None

            try:
                if not inputStr:
                    raise Exception("Input String cannot be empty")

                if inputStr:
                    data = ''.join(e for e in inputStr if e.isalnum())

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
