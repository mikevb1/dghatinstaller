"""Removes old hats in Duck Game directory, moves new ones over."""
from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from tkinter import Tk, filedialog, messagebox
from shutil import copy2 as copy
from datetime import datetime
from sys import argv, exit as exits
import logging as log
from re import match
import os


def exist_check(root, location, name):
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
            folder = folder_select(root, name)
    return folder


def folder_select(root, name):
    """Prompt to select folder.

    Arguments:
    name -- name of folder, to be used in titlebar of window

    Result:
    Return folder user selects.
    Exit if user presses 'Cancel' or closes window.
    """
    folder = filedialog.askdirectory(parent=root,
                                     initialdir='C:\\',
                                     mustexist=True,
                                     title='Select {} directory.'.format(name)
                                     )
    if not folder:
        root.destroy()
        exits(0)
    return folder


def message_box(root, message, icon='info'):
    """Show tkinter message box with message and icon."""
    messagebox.showinfo(parent=root,
                        title=argv[0],
                        message=message,
                        icon=icon
                        )
    root.destroy()


def yes_no(root, text, title=argv[0]):
    """Display box asking yes or no.

    Arguments:
    text -- text displayed in box
    title -- text displayed in titlebar

    Result:
    Return True or False
    Terminates program if user does not select 'yes' or 'no'
    """
    yesno = messagebox.askyesno(title, text)
    if yesno not in [True, False]:
        root.destroy()
        exits(0)
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
    except Exception:
        return None
    steam_dir = EnumValue(steam_reg_key, 1)[1]
    CloseKey(steam_reg_key)
    return steam_dir


def log_name(main=argv[0]):
    """Take name of script and change extension to 'log'."""
    return os.path.splitext(main)[0]+'.log'


def main():
    """Remove any hats in game directory and copies new ones over."""
    root = Tk()
    root.withdraw()

    steam_dir = get_steam_dir()
    if not steam_dir:
        game_dir = folder_select(root, 'Duck Game')
    else:
        game_dir = os.path.join(steam_dir, 'steamapps', 'common', 'Duck Game')
        game_dir = exist_check(root, game_dir, 'Duck Game')

    hat_dir = os.path.join(os.getcwd(), 'hats')
    hat_dir = exist_check(root, hat_dir, 'hat')

    log.basicConfig(filename=log_name(),
                    level=log.INFO,
                    format='%(message)s'
                    )
    log_now = datetime.now().strftime('%d %b %Y - %H:%M:%S')

    log.info('Run Time: %s\n\n', log_now)
    if yes_no(root, 'Remove currently installed hats?\n\n'
              'Any currently installed hats with names matching\n'
              "new hats WILL be overwritten if you select 'No'."):
        log.info('Removing files:')
        for f in os.listdir(game_dir):
            if match('.*\.hat', f) or f == 'hatcredits.txt':
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
        log.info('%s %s %s',
                 srcfile,
                 'OVERWRITING' if exists else '->',
                 destfile
                 )
        exists = False
    log.info('\n\n--------------------------------------------------\n\n')

    message_box(root, 'All done!\nNew hats should be installed.')

if __name__ == '__main__':
    main()
