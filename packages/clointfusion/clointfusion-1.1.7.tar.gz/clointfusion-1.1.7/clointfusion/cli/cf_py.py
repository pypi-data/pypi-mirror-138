from clointfusion.check_system import os_name, windows_os, mac_os, linux_os, python_version, python_37, python_38, python_39, python_310, report_error, python_exe_path_ut, python_exe_path


import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
def main():
    import random
    import os
    """Open python interpreter with preloaded clointfusion as cf."""

    functions_list = ['message_counter_down_timer', 'message_pop_up', 'message_flash', 'message_toast', 'mouse_click', 'mouse_move', 'mouse_drag_from_to', 'mouse_search_snip_return_coordinates_x_y', 'key_press', 'key_write_enter', 'key_hit_enter', 'browser_activate', 'folder_read_text_file', 'folder_write_text_file', 'folder_create', 'folder_create_text_file', 'folder_get_all_filenames_as_list', 'folder_delete_all_files', 'file_rename', 'window_show_desktop',
                      'window_get_all_opened_titles_windows', 'window_activate_and_maximize_windows', 'window_minimize_windows', 'window_close_windows', 'launch_any_exe_bat_application', 'string_extract_only_alphabets', 'string_extract_only_numbers', 'string_remove_special_characters', 'scrape_save_contents_to_notepad', 'scrape_get_contents_by_search_copy_paste', 'pause_program', 'show_emoji', 'clear_screen', 'print_with_magic_color', 'text_to_speech', 'speech_to_text']
    ch_function_1 = random.choice(functions_list)
    ch_function_2 = random.choice(functions_list)
    ch_function_3 = random.choice(functions_list)

    if os_name == windows_os:
        os.system(f'{python_exe_path}')
        # os.system(f'"{python_exe_path_ut}" -i -c "import clointfusion as cf; print(\'Try some of our functions | cf.{ch_function_1}() | or | cf.{ch_function_2}() | or | cf.{ch_function_3}() |\')"')
    elif os_name == linux_os:
        os.system(f'sudo python{python_version} -i -c "import clointfusion as cf; print(\'Try some of our functions | cf.{ch_function_1}() | or | cf.{ch_function_2}() | or | cf.{ch_function_3}() |\')"')
    else:
        try:
            os.system(f'python{python_version} -i -c "import clointfusion as cf; print(\'Try some of our functions | cf.{ch_function_1}() | or | cf.{ch_function_2}() | or | cf.{ch_function_3}() |\')"')
        except:
            print("This command is not available on macOS.")
            print(
                f"Please contribute to make this feature available on {os_name.upper()} system.")
            # print(random.choice(contribution_messages))
            # selft.crash_report(traceback.format_exception(*sys.exc_info(),limit=None, chain=True))
