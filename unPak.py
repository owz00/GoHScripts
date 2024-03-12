from tqdm import tqdm
import time
from zipfile import ZipFile
import shutil
import os
from pathlib import Path


toProgramfiles= "Programfiles(X86)"
gameDir = 'Steam\steamapps\common\Call to Arms - Gates of Hell\mods'
modDirectory = 'template'

prgm_path = os.environ.get(toProgramfiles)

os.chdir(prgm_path)
os.chdir(gameDir)
os.chdir(f"./{modDirectory}")
os.chdir("resource/entity")

if os.path.exists("./-vehicle.pak"):
        print("yes")
        with ZipFile('-vehicle.pak',"r") as zip_ref:
                for file in tqdm(iterable=zip_ref.namelist(), total=len(zip_ref.namelist())):
                    zip_ref.extract(member=file)
        os.remove("-vehicle.pak")
                    
     
#python maps



