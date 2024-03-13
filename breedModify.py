import re
import os
import pandas as pd
import math




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
        



def main():
 
    game_dir = 'Steam/steamapps/common/Call to Arms - Gates of Hell/mods/template'
    os.chdir(os.path.join(os.environ.get("ProgramFiles(X86)"), game_dir))
    excelSheet = 'GoHBreeds.xlsx'
    df=pd.read_excel(excelSheet)
    filePaths = df['filePath'].values
    
    #warning- the order of this array is important
    array = df[['Veterancy', 'Rifle Skill', 'Smg Skill', 'At Skill', 'Loader Skill', 'Mg Skill', 'Smg Loader Skill']].values.tolist()
  
    print("updating Files")
    for file, values in zip(filePaths, array):
        updateFile(file, values)
    print("update Complete")
 
  
if __name__ == "__main__":
    main()
