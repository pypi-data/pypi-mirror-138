__version__ = '1.1.7'
__author__ = 'ClointFusion'
__email__ = 'clointfusion@cloint.com'

from clointfusion.check_system import is_supported, env_var_verify

compatible_system = is_supported()
env_var_verified = env_var_verify()

if compatible_system and env_var_verified:
    # ---------  Message  Functions | Current Count : 4
    from clointfusion.clointfusion import message_counter_down_timer
    from clointfusion.clointfusion import message_pop_up
    from clointfusion.clointfusion import message_flash
    from clointfusion.clointfusion import message_toast

    # ---------  Mouse Functions | Current Count : 4
    from clointfusion.clointfusion import mouse_click
    from clointfusion.clointfusion import mouse_move
    from clointfusion.clointfusion import mouse_drag_from_to
    from clointfusion.clointfusion import mouse_search_snip_return_coordinates_x_y

    # ---------  Keyboard Functions | Current Count : 3
    from clointfusion.clointfusion import key_press
    from clointfusion.clointfusion import key_write_enter
    from clointfusion.clointfusion import key_hit_enter

    # ---------  Browser Functions | Current Count : 1
    from clointfusion.clointfusion import ChromeBrowser
    
    # ---------  Folder Functions | Current Count : 8
    from clointfusion.clointfusion import folder_read_text_file
    from clointfusion.clointfusion import folder_write_text_file
    from clointfusion.clointfusion import folder_create
    from clointfusion.clointfusion import folder_create_text_file
    from clointfusion.clointfusion import folder_get_all_filenames_as_list
    from clointfusion.clointfusion import folder_delete_all_files
    from clointfusion.clointfusion import file_rename
    from clointfusion.clointfusion import file_get_json_details

    # ---------  Window Operations Functions | Current Count : 6
    from clointfusion.clointfusion import window_show_desktop
    from clointfusion.clointfusion import window_get_all_opened_titles_windows
    from clointfusion.clointfusion import window_activate_and_maximize_windows
    from clointfusion.clointfusion import window_minimize_windows
    from clointfusion.clointfusion import window_close_windows
    from clointfusion.clointfusion import launch_any_exe_bat_application

    # ---------  String Functions | Current Count : 3
    from clointfusion.clointfusion import string_extract_only_alphabets
    from clointfusion.clointfusion import string_extract_only_numbers
    from clointfusion.clointfusion import string_remove_special_characters

    # --------- Screenscraping Functions | Current Count : 5
    from clointfusion.clointfusion import scrape_save_contents_to_notepad
    from clointfusion.clointfusion import screen_clear_search
    from clointfusion.clointfusion import search_highlight_tab_enter_open
    from clointfusion.clointfusion import find_text_on_screen

    # --------- Utility Functions | Current Count : 7
    from clointfusion.clointfusion import find
    from clointfusion.clointfusion import pause_program
    from clointfusion.clointfusion import show_emoji
    from clointfusion.clointfusion import download_this_file
    from clointfusion.clointfusion import clear_screen
    from clointfusion.clointfusion import print_with_magic_color


    # --------- Voice Interface | Current Count : 2
    from clointfusion.clointfusion import text_to_speech
    from clointfusion.clointfusion import speech_to_text