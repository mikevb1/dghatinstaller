from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM #to get steam install location
from shutil import copy2 as copy
from tkinter import Tk, filedialog
from sys import exit
import os
import re

def exist_check(location,name):
    folder = location
    while True:
        try:
            os.stat(folder)
            break
        except FileNotFoundError:
            if name == 'Steam':
                return False
            folder = folder_select(name)
    return True

def folder_select(name):
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(parent=root,
                                     initialdir='C:\\',
                                     mustexist=True,
                                     title='Select {} directory.'.format(name)
                                     )
    root.destroy()
    return folder

def main():
    steam_reg_key = OpenKey(HKLM,'SOFTWARE\\WOW6432Node\\Valve\\Steam')
    steam_dir = EnumValue(steam_reg_key,1)[1]
    CloseKey(steam_reg_key)
    if !exist_check(steam_dir,'Steam'):
        game_dir = folder_select('Duck Game')
    else:
        game_dir = '{}\\steamapps\\common\\Duck Game'.format(steam_dir)
        exist_check('{}\\DuckGame.exe'.format(game_dir),'Duck Game')

    hat_dir = '{}\\hats'.format(os.getcwd())
    exist_check(hat_dir,'hat')

    for f in os.listdir(game_dir):
        if re.match('.*\.hat',f) or f == 'hatcredits.txt':
            os.remove(f)
    for f in os.listdir(hat_dir):
        srcfile = '{}\\{}'.format(hat_dir,f)
        copy(srcfile,game_dir)

    print('Your new hats should now be ready! If they\'re not, go yell at sgtlaggy.')

if __name__ == '__main__':
    main()
