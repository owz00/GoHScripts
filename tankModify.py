import re
import os
import pandas as pd


def updateFile(FirstfileName, newValue):
    fileString = ""
    newValue = str(newValue)
   
    with open(FirstfileName) as file:
        lines = file.readlines()
        for line in lines:
            fileString += line
    
    match = re.search(r'(bone.*?turret.*?speed2.*?.)(\d*\.?\d+)(.*)',   fileString, re.DOTALL)  
    newString = (match.group(1)+ newValue + match.group(3))

    with open(FirstfileName, "r+") as file:
        file.truncate(0)
        file.write(newString)
      
    return newString




def updateRotationSpeed(fileName, newValue):

    fileString = ""
    with open(fileName) as file:
        lines = file.readlines()
        for line in lines:
            fileString += line

    patterns = [
        (r'(.*mass.*?bone.*?turret.*?speed2.*?)(-?\d*\.?\d+)(.*)', None, None),
        (r'(.*turret_light.*?power_traverse.*?)(-?\d*\.?\d+)(.*)', 10, 2.5),
        (r'(.*turret_medium.*?power_traverse.*?)(-?\d*\.?\d+)(.*)', 6, 2.5),
        (r'(.*turret_heavy.*?power_traverse.*?)(-?\d*\.?\d+)(.*)', 4, 3)
    ]

    for pattern, base, multiplier in patterns:
        match = re.search(pattern, fileString, re.DOTALL)
        if match:
            if base is not None and multiplier is not None:
                newValue = str((newValue - base) * multiplier)   
          
            fileString = (match.group(1) + str(newValue) + match.group(3))
            with open(fileName, "r+") as file:
                    file.truncate(0)
                    file.write(fileString)
    return fileString




def updateFile(fileName, newValueArray):

    fileString = ""
    with open(fileName) as file:
        lines = file.readlines()
        for line in lines:
            fileString += line

    #warning- the order of this array is important 
    patterns = [r'(.*mobility_tank.*?speed.*?)(-?\d*\.?\d+)(.*)',#"maxSpeed"
                r'(.*mobility_tank.*?reverse.*?)(-?\d*\.?\d+)(.*)',#"reverseSpeed"
                r'(.*mobility_tank.*?traverse.*?)(-?\d*\.?\d+)(.*)',#"traverseSpeed"
                r'(.*mobility_tank.*?weight.*?)(-?\d*\.?\d+)(.*)',#"weight"
                r'(.*mobility_tank.*?power.*?)(-?\d*\.?\d+)(.*)',#"enginePower"
                r'(.*mobility_tank.*?track.*?)(-?\d*\.?\d+)(.*)',#"trackPerformance"
                r'(.*mobility_tank.*?fuel.*?)(-?\d*\.?\d+)(.*)',#"fuelCapacity"
                r'(.*mobility_tank.*?type.*?\()(.*?)(\).*)',#"fuelType"
                r'(.*gun_rot.*?speed2.*?)(-?\d*\.?\d+)(.*)',#"gunRotSpeed"
                r'(.*inventory.*?\ apcbche.*?)(-?\d*\.?\d+)(.*)',#"apcbcheAmmo"
                r'(.*inventory.*?\ he.*?)(-?\d*\.?\d+)(.*)',#"heAmmo"
                r'(.*inventory.*?\ heat.*?)(-?\d*\.?\d+)(.*)',#"heatAmmo"
                r'(.*inventory.*?\ aphebc.*?)(-?\d*\.?\d+)(.*)',#"aphebcAmmo"
               ]
    
    for value, pattern in zip(newValueArray, patterns):
        match = re.search(pattern, fileString, re.DOTALL)
        if match:
            fileString = match.group(1) + str(value) + match.group(3)

        with open(fileName, "r+") as file:
            file.truncate(0)
            file.write(fileString)
    return fileString
        



def main():
 
    game_dir = 'Steam/steamapps/common/Call to Arms - Gates of Hell/mods/template'
    os.chdir(os.path.join(os.environ.get("ProgramFiles(X86)"), game_dir))

    excelSheet = 'GoHStats.xlsx'

    df=pd.read_excel(excelSheet)
    filePaths = df['filePaths'].values
    turretRotSpeed = df['turretRotSpeed'].values.astype(int)
    #warning- the order of this array is important
    array = df[['maxSpeed','reverseSpeed', 'traverseSpeed', 'weight', 'enginePower', 'trackPerformance', 
                'fuelCapacity', 'fuelType','gunRotSpeed','apcbcheAmmo','heAmmo','heatAmmo','aphebcAmmo']].values.tolist()
 
    print("updating general data")
    for file, values in zip(filePaths, array):
        updateFile(file, values)
       
    print("updating turret rotation speeds")
    for file, turretRotationSpeed in zip(filePaths, turretRotSpeed):
        updateRotationSpeed(file, turretRotationSpeed)
    print("turret rotation speed successfully updated")      

  
if __name__ == "__main__":
    main()

