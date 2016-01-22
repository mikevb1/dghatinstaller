from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from shutil import copy2 as copy
from tkinter import Tk, filedialog
from sys import exit
import os
import re


def exist_check(location, name):
    folder = location
    while True:
        if os.path.isdir(folder):
            break
        else:
            folder = folder_select(name)
    return folder


def folder_select(name):
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


def get_steam_dir():
    try:
        steam_reg_key = OpenKey(HKLM, 'SOFTWARE\\WOW6432Node\\Valve\\Steam')
    except FileNotFoundError:
        steam_reg_key = OpenKey(HKLM, 'SOFTWARE\\Valve\\Steam')
    except:
        return
    steam_dir = EnumValue(steam_reg_key, 1)[1]
    CloseKey(steam_reg_key)
    return steam_dir


def main():
    steam_dir = get_steam_dir()
    if not steam_dir:
        game_dir = folder_select('Duck Game')
    else:
        game_dir = '{}\\steamapps\\common\\Duck Game'.format(steam_dir)
        game_dir = exist_check(game_dir, 'Duck Game')

    hat_dir = '{}\\hats'.format(os.getcwd())
    hat_dir = exist_check(hat_dir, 'hat')

    log = open('hats.log', 'w')
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
        log.write(srcfile + ' -> ' + destfile + '\n')
    log.close()

    print('Your new hats should now be ready!')
    input('Press ENTER to exit.')

if __name__ == '__main__':
    main()
