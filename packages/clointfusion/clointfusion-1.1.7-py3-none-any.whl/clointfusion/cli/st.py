try:
    from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error, python_exe_path
    from clointfusion.clointfusion import contribution_messages
except:
    from check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error, python_exe_path
    from clointfusion import contribution_messages

import random
import os
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
def main():
    """CLI for testing internet bandwidth using speedtest.net"""
    try:
        if os_name != mac_os:
            print(os.system("speedtest-cli"))
        else:
            try:
                print(os.system("speedtest-cli"))
            except:
                print(
                    "This feature is curently not supported on macOS. Please contribute to make the tomorrow better.")
                print(random.choice(contribution_messages))
    except Exception as ex:
        report_error(ex)
