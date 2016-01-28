"""Removes old hats in Duck Game directory, moves new ones over."""
from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from tkinter import Tk, filedialog, messagebox
from shutil import copy2 as copy
from sys import argv, exit
import datetime as dt
import os
import re


def exist_check(location, name):
    """Check whether location exists and prompts for location if it does not.

    Arguments:
    location -- location of folder found relative to program or from registry
    name -- name of folder, only used when location does not exist

    Result:
    Return valid folder path.
    """
    folder = location
    while True:
        if os.path.isdir(folder):
            break
        else:
            folder = folder_select(name)
    return folder


def folder_select(name):
    """Prompt for a new location if originally found location does not exist.

    Arguments:
    name -- name of folder, to be used in titlebar of window

    Result:
    Return folder user selects.
    Exit if user presses 'Cancel' or closes window.
    """
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(parent=root,
                                     initialdir='C:\\',
                                     mustexist=True,
                                     title='Select {} directory.'.format(name)
                                     )
    root.destroy()
    if not folder:
        exit(0)
    return folder


def done_box():
    """Display box saying program is done."""
    root = Tk()
    root.withdraw()
    messagebox.showinfo(argv[0],
                        'All done.\nNew hats should be installed.'
                        )
    root.destroy()
    exit(0)


def get_steam_dir():
    """Get steam install directory from registry.

    Result:
    Return Steam install directory.
    Return nothing if neither registry key doesn't exist.
    """
    try:
        steam_reg_key = OpenKey(HKLM, 'SOFTWARE\\WOW6432Node\\Valve\\Steam')
    except FileNotFoundError:
        steam_reg_key = OpenKey(HKLM, 'SOFTWARE\\Valve\\Steam')
    except:
        return
    steam_dir = EnumValue(steam_reg_key, 1)[1]
    CloseKey(steam_reg_key)
    return steam_dir


def log_from_main(main=argv[0]):
    """Take name of script and change extension to 'log'."""
    log = list(main)
    while log[-1] != '.':
        log.pop()
    log.append('log')
    log = ''.join(log)
    return log


def main():
    """Remove any hats in game directory and copies new ones over."""
    steam_dir = get_steam_dir()
    if not steam_dir:
        game_dir = folder_select('Duck Game')
    else:
        game_dir = '{}\\steamapps\\common\\Duck Game'.format(steam_dir)
        game_dir = exist_check(game_dir, 'Duck Game')

    hat_dir = '{}\\hats'.format(os.getcwd())
    hat_dir = exist_check(hat_dir, 'hat')

    log_file = log_from_main()
    log_now = dt.datetime.now().strftime('%d %b %Y - %H:%M:%S')

    with open(log_file, 'a') as log:
        log.write('Run Time: {}\n\n'.format(log_now))
        log.write('Removing files:\n')
        for f in os.listdir(game_dir):
            if re.match('.*\.hat', f) or f == 'hatcredits.txt':
                os.remove('{}\\{}'.format(game_dir, f))
                log.write('{}\\{}'.format(game_dir, f) + '\n')
        log.write('\nCopying files:\n')
        for f in os.listdir(hat_dir):
            srcfile = '{}\\{}'.format(hat_dir, f)
            destfile = '{}\\{}'.format(game_dir, f)
            copy(srcfile, destfile)
            log.write('{} -> {}\n'.format(srcfile, destfile))
        log.write('\n----------\n\n')

    done_box()

if __name__ == '__main__':
    main()
