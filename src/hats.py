"""Removes old hats in Duck Game directory, moves new ones over."""
from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from tkinter import Tk, filedialog, messagebox
from sys import argv, exit as exits
from shutil import copy2 as copy
from datetime import datetime
import logging as log
from re import match
import os

# log.X where X is DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = log.INFO


def exist_check(root: Tk, location: str, name: str) -> str:
    """Check whether location exists and prompt for location if it does not.

    Arguments:
    root -- Tk root window to bind to
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
    log.debug('%s: %s dir: %s\n', 'exist_check()', name, folder)
    return folder


def folder_select(root: Tk, name: str) -> str:
    """Prompt to select folder.

    Arguments:
    root -- Tk root window to bind to
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
    log.debug('%s: folder: %s\n', 'folder_select()', folder)
    return folder


def message_box(root: Tk, message: str,
                title: str =argv[0], icon: str ='info') -> None:
    """Show tkinter message box with message and icon.

    Arguments:
    root -- Tk root window to bind to
    message -- message to be shown
    title -- text displayed in titlebar
    icon -- icon to be shown in ['info','warning','error','question']
    """
    messagebox.showinfo(parent=root,
                        title=title,
                        message=message,
                        icon=icon
                        )


def yes_no(root: Tk, text: str, title: str =argv[0]) -> str:
    """Display box asking yes or no.

    Arguments:
    root -- Tk root window to bind to
    text -- text displayed in box
    title -- text displayed in titlebar

    Result:
    Return True or False
    Terminates program if user does not select 'yes' or 'no'
    """
    yesno = messagebox.askyesno(title, text)
    if yesno not in [True, False]:
        log.critical('%s: answer: %s\n', 'yes_no()', yesno)
        root.destroy()
        exits(0)
    return yesno


def get_steam_dir() -> str:
    """Get steam install directory from registry.

    Result:
    Return Steam install directory.
    Return nothing if neither registry key exists.
    """
    try:
        steam_reg_key = OpenKey(HKLM, 'SOFTWARE\\WOW6432Node\\Valve\\Steam')
    except FileNotFoundError:
        steam_reg_key = OpenKey(HKLM, 'SOFTWARE\\Valve\\Steam')
    except Exception as e:
        log.warning('%s: Could not get Steam install location.\n', 'WARNING')
        log.debug('%s: %s: Exception: %s', 'DEBUG', 'get_steam_dir()', e)
        return ''
    steam_dir = EnumValue(steam_reg_key, 1)[1]
    CloseKey(steam_reg_key)
    return steam_dir


def log_name(main: str =argv[0]) -> str:
    """Take name of script and change extension to 'log'."""
    return os.path.splitext(main)[0] + '.log'


def main() -> None:
    """Remove any hats in game directory and copies new ones over."""
    log.basicConfig(filename=log_name(),
                    level=LOG_LEVEL,
                    format='%(message)s'
                    )
    log_now = datetime.now().strftime('%d %b %Y - %H:%M:%S')
    log.info('Run Time: %s\n\n', log_now)

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

    log.debug('Steam dir: %s\nGame dir: %s\nHat dir: %s\n',
              steam_dir,
              game_dir,
              hat_dir
              )

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
    log.info('\n\n%s\n\n', '-' * 100)

    message_box(root, 'All done!\nNew hats should be installed.')

    root.destroy()

if __name__ == '__main__':
    main()
