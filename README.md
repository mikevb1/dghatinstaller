Icon file used with permission of its original creator, [/u/BeardedBears](https://www.reddit.com/user/BeardedBears).

Current hat pack [here](https://drive.google.com/open?id=0B36t-wx7lxZALUtScDJUOU9sWnM). No permission from creators, but credits are given.

Using hats.exe will remove any hats you currently have and will copy the ones from this pack over.
hats.exe will work only if you have Duck Game installed in Steam's install directory.

If you don't want to use hats.exe you can copy the contents of the "hats" folder to the
Duck Game install directory. All the .hat files should end up in the same folder as DuckGame.exe.

If you use hats.exe, you must have the following folder structure or you will be asked for file locations.
If a file selection box comes up, look at the titlebar to see what folder to select.
You will only be asked to select your Duck Game install directory or the folder that contains the .hat files.

    any folder\
                hats\
                     hat1.hat
                     hat2.hat
                     ...
                hats.exe

#Building
To compile this to .exe, I use Pyinstaller.

On first build:

    pyinstaller -Fwi icon.ico  hats.py

After hats.spec has been created, and on subsequent builds:

    pyinstaller hats.spec
