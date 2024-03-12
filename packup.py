import shutil
import time
from zipfile import ZipFile
import subprocess
import os
import shlex

import traceback





toProgramfiles= "Programfiles(X86)"
gameDir = 'Steam\steamapps\common\Call to Arms - Gates of Hell\mods'
modDirectory = 'template'

prgm_path = os.environ.get(toProgramfiles)





# go in resource
os.chdir(prgm_path)
os.chdir(gameDir)
os.chdir(f"./{modDirectory}")
os.chdir("resource/entity")
# paks
if os.path.exists("./-vehicle"):
    #print("yes")
    subprocess.call(shlex.split(f"C:/Program Files/7-Zip/7z.exe a  vehicle.pak ./-vehicle -mx=7 -mmt=16 -sdel -tzip"))
    os.rename('vehicle.pak', '-vehicle.pak')