from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE as HKLM
from shutil import copy2 as copy
from sys import exit
import os
import re

steam_reg_key = OpenKey(HKLM,'SOFTWARE\\WOW6432Node\\Valve\\Steam')
steam_dir = EnumValue(steam_reg_key,1)[1]
CloseKey(steam_reg_key)
try:
    os.stat(steam_dir)
except FileNotFoundError:
    print('Could not find Steam folder.')
    input('Press ENTER to exit.')
    exit(0)

game_dir = '{}\\steamapps\\common\\Duck Game'.format(steam_dir)
try:
    os.stat('{}\\DuckGame.exe'.format(game_dir))
except FileNotFoundError:
    print('Could not find Duck Game folder. It is likely installed in a secondary Steam library folder.')
    input('Press ENTER to exit.')
    exit(0)

try:
    hat_dir = '{}\\hats'.format(os.getcwd())
    os.stat(hat_dir)
except FileNotFoundError:
    print('There should be a "hats" folder here with .hat files inside.')
    input('Press ENTER to exit.')
    exit(0)

for f in os.listdir(game_dir):
    if re.match('.*\.hat',f) or f == 'hatcredits.txt':
        os.remove(f)
for f in os.listdir(hat_dir):
    srcfile = '{}\\{}'.format(hat_dir,f)
    copy(srcfile,game_dir)

print('Your new hats should now be ready! If they\'re not, go yell at sgtlaggy.')
