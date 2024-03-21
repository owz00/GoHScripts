import re
import os
import pandas as pd
import math
import tkinter as tk
from tkinter import simpledialog
import csv



def updateFile(fileName, newValueArray):

    fileString = ""
    with open(fileName) as file:
        lines = file.readlines()
        for line in lines:
            fileString += line

    #warning- the order of this array is important 
    patterns = [r'(.*veterancy_lvl_)(-?\d*\.?\d+)(.*)',##"veterancy 
                r'(.*rifle_skill_rank_)(-?\d*\.?\d+)(.*)', #"Rifle Skill",
                r'(.*smg_skill_rank_)(-?\d*\.?\d+)(.*)', #"Smg Skill",
                r'(.*at_rank_)(-?\d*\.?\d+)(.*)', #"At Skill",
                r'(.*loader_skill_rank_)(-?\d*\.?\d+)(.*)',# "Loader Skill"
                r'(.*mg_skill_rank_)(-?\d*\.?\d+)(.*)',# "Mg Skill",
                r'(.*loader_skill_smg_rank_)(-?\d*\.?\d+)(.*)', #"Smg Loader Skill")
               ]
    
    for value, pattern in zip(newValueArray, patterns):
        match = re.search(pattern, fileString, re.DOTALL)
        if match:
            fileString = match.group(1) + str(math.trunc(value)) + match.group(3)

        with open(fileName, "r+") as file:
            file.truncate(0)
            file.write(fileString)

    return fileString
        
def interface():
    ROOT = tk.Tk()
    ROOT.withdraw()
   # the input dialog
    USER_INP = simpledialog.askstring(title="Input",
            prompt="Input mod name as is written in its GoH directory")
    CSV_FILE = simpledialog.askstring(title="Input",
            prompt="Input csv file name with its file extension")
    # check it 
    return USER_INP, CSV_FILE


def main():
 
    modName, csvFile = interface()
    game_dir = f'Steam/steamapps/common/Call to Arms - Gates of Hell/mods/{modName}'

    try:
       os.chdir(os.path.join(os.environ.get("ProgramFiles(X86)"), game_dir))
    except FileNotFoundError:
       print("Directory not found.")
       exit()
    except Exception as e:
       print("An error occurred:", e)
       exit()

    try:
        df = pd.read_csv(csvFile)
    except Exception:
        try:
            df = pd.read_excel(csvFile)
        except FileNotFoundError:
            print("File not found.")
            exit()
        except Exception as e:
            print("An error occurred:", e)
            exit()

    filePaths = df['filePath'].values
    #warning- the order of this array is important
    array = df[['Veterancy', 'Rifle Skill', 'Smg Skill', 'At Skill', 'Loader Skill', 'Mg Skill', 'Smg Loader Skill']].values.tolist()
  
    print("updating Files")
    for file, values in zip(filePaths, array):
        updateFile(file, values)
    print("update Complete")
 
  
if __name__ == "__main__":
    main()
