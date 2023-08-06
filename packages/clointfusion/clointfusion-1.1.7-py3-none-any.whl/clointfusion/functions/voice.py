import imp
from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310,python_exe_path_ut, report_error

# Functions Represent in this file


if os_name == windows_os:

    # Windows OS - Python 3.7
    if python_version == python_37:

        def speech_to_text():

            # import section
            try:
                import pyaudio
            except ModuleNotFoundError:
                import os
                cmd = 'https://github.com/ClointFusion/Image_ICONS_GIFs/blob/main/Wheels/PyAudio-0.2.11-cp37-cp37m-win_amd64.whl?raw=true'
                os.system(f'"{python_exe_path_ut}" -m pip install ' + cmd)
                import pyaudio
            import speech_recognition as sr
            from clointfusion.clointfusion import clear_screen
            from clointfusion.clointfusion import text_to_speech
            import sys

            """
            Speech to Text using Google's Generic API
            """

            recognizer = sr.Recognizer()
            energy_threshold = [3000]

            try:
                while True:
                    with sr.Microphone() as source:
                        recognizer.dynamic_energy_threshold = True
                        if recognizer.energy_threshold in energy_threshold or recognizer.energy_threshold <= \
                                sorted(energy_threshold)[-1]:
                            recognizer.energy_threshold = sorted(
                                energy_threshold)[-1]
                        else:
                            energy_threshold.append(
                                recognizer.energy_threshold)

                        recognizer.pause_threshold = 0.8

                        recognizer.adjust_for_ambient_noise(source)

                        audio = recognizer.listen(source)

                        try:
                            print("Speak now !!!")
                            query = recognizer.recognize_google(audio)
                            print(f"You Said : {query}")
                            return query
                        except AttributeError:
                            print(
                                'Could not find PyAudio or no Microphone input device found. It may be being used by '
                                'another '
                                'application.')
                            text_to_speech(
                                "Could not find PyAudio or no Microphone input device found. It may be being used by "
                                "another "
                                "application.")
                            sys.exit()
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print("Try Again")

                        # Windows OS - Python 3.8
            except Exception as ex:
                report_error(ex)

        def text_to_speech(audio, show=True, rate=170):

            # import section
            import pyttsx3
            import random

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice = random.choice(voices)  # Randomly decide male/female voice
            engine.setProperty('voice', voice.id)

            status = False

            try:
                if type(audio) is list:
                    if show:
                        print(' '.join(audio))
                else:
                    if show:
                        print(str(audio))
                if os_name == linux_os:
                    rate -= 10
                engine.setProperty('rate', rate)
                engine.say(audio)
                engine.runAndWait()

            except Exception as ex:
                report_error(ex)

            else:
                status = True
            finally:
                return status


    elif python_version == python_38:

        def speech_to_text():
            
            # import section
            try:
                import pyaudio
            except ModuleNotFoundError:
                import os
                cmd = 'https://github.com/ClointFusion/Image_ICONS_GIFs/blob/main/Wheels/PyAudio-0.2.11-cp38-cp38-win_amd64.whl?raw=true'
                os.system(f'"{python_exe_path_ut}" -m pip install ' + cmd)
                import pyaudio
            import speech_recognition as sr
            from clointfusion.clointfusion import clear_screen
            from clointfusion.clointfusion import text_to_speech
            import sys

            """
            Speech to Text using Google's Generic API
            """

            recognizer = sr.Recognizer()
            energy_threshold = [3000]

            try:
                while True:
                    with sr.Microphone() as source:
                        recognizer.dynamic_energy_threshold = True
                        if recognizer.energy_threshold in energy_threshold or recognizer.energy_threshold <= \
                                sorted(energy_threshold)[-1]:
                            recognizer.energy_threshold = sorted(
                                energy_threshold)[-1]
                        else:
                            energy_threshold.append(
                                recognizer.energy_threshold)

                        recognizer.pause_threshold = 0.8

                        recognizer.adjust_for_ambient_noise(source)

                        audio = recognizer.listen(source)

                        try:
                            print("Speak now !!!")
                            query = recognizer.recognize_google(audio)
                            print(f"You Said : {query}")
                            return query
                        except AttributeError:
                            print(
                                'Could not find PyAudio or no Microphone input device found. It may be being used by '
                                'another '
                                'application.')
                            text_to_speech(
                                "Could not find PyAudio or no Microphone input device found. It may be being used by "
                                "another "
                                "application.")
                            sys.exit()
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print("Try Again")

                        # Windows OS - Python 3.8
            except Exception as ex:
                report_error(ex)

        def text_to_speech(audio, show=True, rate=170):

            # import section
            import pyttsx3
            import random

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice = random.choice(voices)  # Randomly decide male/female voice
            engine.setProperty('voice', voice.id)

            status = False

            try:
                if type(audio) is list:
                    if show:
                        print(' '.join(audio))
                else:
                    if show:
                        print(str(audio))
                if os_name == linux_os:
                    rate -= 10
                engine.setProperty('rate', rate)
                engine.say(audio)
                engine.runAndWait()

            except Exception as ex:
                report_error(ex)

            else:
                status = True
            finally:
                return status


    # Windows OS - Python 3.9
    elif python_version == python_39:

        def speech_to_text():
            
            # import section
            try:
                import pyaudio
            except ModuleNotFoundError:
                import os
                cmd = 'https://github.com/ClointFusion/Image_ICONS_GIFs/blob/main/Wheels/PyAudio-0.2.11-cp39-cp39-win_amd64.whl?raw=true'
                os.system(f'"{python_exe_path_ut}" -m pip install ' + cmd)
                import pyaudio
            import speech_recognition as sr
            from clointfusion.clointfusion import clear_screen
            from clointfusion.clointfusion import text_to_speech
            import sys

            """
            Speech to Text using Google's Generic API
            """

            recognizer = sr.Recognizer()
            energy_threshold = [3000]

            try:
                while True:
                    with sr.Microphone() as source:
                        recognizer.dynamic_energy_threshold = True
                        if recognizer.energy_threshold in energy_threshold or recognizer.energy_threshold <= \
                                sorted(energy_threshold)[-1]:
                            recognizer.energy_threshold = sorted(
                                energy_threshold)[-1]
                        else:
                            energy_threshold.append(
                                recognizer.energy_threshold)

                        recognizer.pause_threshold = 0.8

                        recognizer.adjust_for_ambient_noise(source)

                        audio = recognizer.listen(source)

                        try:
                            print("Speak now !!!")
                            query = recognizer.recognize_google(audio)
                            print(f"You Said : {query}")
                            return query
                        except AttributeError:
                            print(
                                'Could not find PyAudio or no Microphone input device found. It may be being used by '
                                'another '
                                'application.')
                            text_to_speech(
                                "Could not find PyAudio or no Microphone input device found. It may be being used by "
                                "another "
                                "application.")
                            sys.exit()
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print("Try Again")

                        # Windows OS - Python 3.8
            except Exception as ex:
                report_error(ex)

        def text_to_speech(audio, show=True, rate=170):

            # import section
            import pyttsx3
            import random

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice = random.choice(voices)  # Randomly decide male/female voice
            engine.setProperty('voice', voice.id)

            status = False

            try:
                if type(audio) is list:
                    if show:
                        print(' '.join(audio))
                else:
                    if show:
                        print(str(audio))
                if os_name == linux_os:
                    rate -= 10
                engine.setProperty('rate', rate)
                engine.say(audio)
                engine.runAndWait()

            except Exception as ex:
                report_error(ex)

            else:
                status = True
            finally:
                return status


    # Windows OS - Python 3.10
    elif python_version == python_310:

        def speech_to_text():
            
            # import section
            try:
                import pyaudio
            except ModuleNotFoundError:
                import os
                cmd = 'https://download.lfd.uci.edu/pythonlibs/x6hvwk7i/PyAudio-0.2.11-cp310-cp310-win_amd64.whl'
                os.system(f'"{python_exe_path_ut}" -m pip install ' + cmd)
                import pyaudio
            import speech_recognition as sr
            from clointfusion.clointfusion import clear_screen
            from clointfusion.clointfusion import text_to_speech
            import sys

            """
            Speech to Text using Google's Generic API
            """

            recognizer = sr.Recognizer()
            energy_threshold = [3000]

            try:
                while True:
                    with sr.Microphone() as source:
                        recognizer.dynamic_energy_threshold = True
                        if recognizer.energy_threshold in energy_threshold or recognizer.energy_threshold <= \
                                sorted(energy_threshold)[-1]:
                            recognizer.energy_threshold = sorted(
                                energy_threshold)[-1]
                        else:
                            energy_threshold.append(
                                recognizer.energy_threshold)

                        recognizer.pause_threshold = 0.8

                        recognizer.adjust_for_ambient_noise(source)

                        audio = recognizer.listen(source)

                        try:
                            print("Speak now !!!")
                            query = recognizer.recognize_google(audio)
                            print(f"You Said : {query}")
                            return query
                        except AttributeError:
                            print(
                                'Could not find PyAudio or no Microphone input device found. It may be being used by '
                                'another '
                                'application.')
                            text_to_speech(
                                "Could not find PyAudio or no Microphone input device found. It may be being used by "
                                "another "
                                "application.")
                            sys.exit()
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print("Try Again")

                        # Windows OS - Python 3.8
            except Exception as ex:
                report_error(ex)

        def text_to_speech(audio, show=True, rate=170):

            # import section
            import pyttsx3
            import random

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice = random.choice(voices)  # Randomly decide male/female voice
            engine.setProperty('voice', voice.id)

            status = False

            try:
                if type(audio) is list:
                    if show:
                        print(' '.join(audio))
                else:
                    if show:
                        print(str(audio))
                if os_name == linux_os:
                    rate -= 10
                engine.setProperty('rate', rate)
                engine.say(audio)
                engine.runAndWait()

            except Exception as ex:
                report_error(ex)

            else:
                status = True
            finally:
                return status


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
