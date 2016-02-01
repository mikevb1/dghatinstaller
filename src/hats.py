"""Removes old hats in Duck Game directory, moves new ones over."""
from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from tkinter import Tk, filedialog, messagebox
from shutil import copy2 as copy
from sys import argv, exit
import datetime as dt
import logging as log
import os
import re


def exist_check(location, name):
    """Check whether location exists and prompt for location if it does not.

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
    """Prompt to select folder.

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


def yes_no(text, title=argv[0]):
    """Display box asking yes or no.

    Arguments:
    text -- text displayed in box
    title -- text displayed in titlebar

    Result:
    Return True or False
    Terminates program if user does not select 'yes' or 'no'
    """
    root = Tk()
    root.withdraw()
    yesno = messagebox.askyesno(title, text)
    root.destroy()
    if yesno not in [True, False]:
        exit(0)
    return yesno


def get_steam_dir():
    """Get steam install directory from registry.

    Result:
    Return Steam install directory.
    Return nothing if neither registry key exists.
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


def log_name(main=argv[0]):
    """Take name of script and change extension to 'log'."""
    return os.path.splitext(main)[0]+'.log'


def main():
    """Remove any hats in game directory and copies new ones over."""
    steam_dir = get_steam_dir()
    if not steam_dir:
        game_dir = folder_select('Duck Game')
    else:
        game_dir = os.path.join(steam_dir, 'steamapps', 'common', 'Duck Game')
        game_dir = exist_check(game_dir, 'Duck Game')

    hat_dir = os.path.join(os.getcwd(), 'hats')
    hat_dir = exist_check(hat_dir, 'hat')

    log.basicConfig(filename=log_name(),
                    level=log.INFO,
                    style='{',
                    format='{message}'
                    )
    log_now = dt.datetime.now().strftime('%d %b %Y - %H:%M:%S')

    log.info('Run Time: {}\n\n'.format(log_now))
    if yes_no('Remove currently installed hats?\n\n'
              'Any currently installed hats with names matching\n'
              "new hats WILL be overwritten if you select 'No'."):
        log.info('Removing files:')
        for f in os.listdir(game_dir):
            if re.match('.*\.hat', f) or f == 'hatcredits.txt':
                os.remove(os.path.join(game_dir, f))
                log.info(os.path.join(game_dir, f))
    else:
        log.info('Not removing files.')
    log.info('\n\nCopying files:')
    exists = False
    for f in os.listdir(hat_dir):
        srcfile = os.path.join(hat_dir, f)
        destfile = os.path.join(game_dir, f)
        if os.path.isfile(destfile):
            exists = True
        copy(srcfile, destfile)
        log.info('{} {} {}'.format(srcfile,
                                   'OVERWRITING' if exists else '->',
                                   destfile))
        exists = False
    log.info('\n\n--------------------------------------------------\n\n')

    done_box()

if __name__ == '__main__':
    main()
