from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from shutil import copy2 as copy
from sys import exit
import os
import re

def check_folder_exist(folder,foldername):
    try:
        os.stat(folder)
    except FileNotFoundError:
        print('Could not find {} folder.'.format(foldername))
        input('Press ENTER to exit.')
        exit(0)

def main():
    steam_reg_key = OpenKey(HKLM,'SOFTWARE\\WOW6432Node\\Valve\\Steam')
    steam_dir = EnumValue(steam_reg_key,1)[1]
    CloseKey(steam_reg_key)
    check_folder_exist(steam_dir,'Steam')

    game_dir = '{}\\steamapps\\common\\Duck Game'.format(steam_dir)
    check_folder_exist('{}\\DuckGame.exe'.format(game_dir),'Duck Game')

    hat_dir = '{}\\hats'.format(os.getcwd())
    check_folder_exist(hat_dir,'hat')

    for f in os.listdir(game_dir):
        if re.match('.*\.hat',f) or f == 'hatcredits.txt':
            os.remove(f)
    for f in os.listdir(hat_dir):
        srcfile = '{}\\{}'.format(hat_dir,f)
        copy(srcfile,game_dir)

    print('Your new hats should now be ready! If they\'re not, go yell at sgtlaggy.')

if __name__ == '__main__':
    main()
