from PyPAKParser import PakParser
import os
import pandas as pd
import re

path = "./resource/entity/-vehicle"


toProgramfiles= "Programfiles(X86)"
gameDir = 'Steam\steamapps\common\Call to Arms - Gates of Hell\mods'
modDirectory = 'template'

prgm_path = os.environ.get(toProgramfiles)

os.chdir(prgm_path)
os.chdir(gameDir)
os.chdir(f"./{modDirectory}")
#os.chdir("resource/entity")





def getTankandCannonEntities():
    turretedArrayFilePaths = []
    print(os.getcwd())
    print(path)
    for root,d_names,f_names in os.walk(path):
            if re.search(r'.*tank((?!x).)*$', root): #or re.search(r'cannon', root): 
              # if re.search(r'.*tank((?!x).)*$', root):
                for file in f_names:
                    if file.endswith(".def"):
                            #print(root, file)
                        filePath = root + "\\" + file
                            #print(filePath)
                        turretedArrayFilePaths.append(filePath)

    return turretedArrayFilePaths

def getTurretRotation(fileString):
    turretRotSpeed  ="N/A"
    patterns = [
        (r'turret_light.*?power_traverse.*?(-?\d*\.?\d+)', 10, 2.5),
        (r'turret_medium.*?power_traverse.*?(-?\d*\.?\d+)', 6, 2.5),
        (r'turret_heavy.*?power_traverse.*?(-?\d*\.?\d+)', 4, 3),
        (r'.*mass.*?bone.*?turret.*?speed2.*?(-?\d*\.?\d+)', None, None),
    ]
     
    for pattern, base, divisor in patterns:
        match = re.search(pattern, fileString, re.DOTALL)
        if match:
            if base is not None and divisor is not None:
                turretRotSpeed = str(base + (float(match.group(1)) / divisor)) 
            else:
               turretRotSpeed = match.group(1)
            break
     
    return turretRotSpeed




def getData(FirstfileName, dictionary):
    fileString = ""
     
    match = re.search(r'(\w*).def?', FirstfileName)
    entityName = match.group(1)
   
    with open(FirstfileName) as file:
        #add all lines of the text file to a string
        lines = file.readlines()
        for line in lines:
              fileString += line

    turretRotSpeed = getTurretRotation(fileString)
    patterns = [(r'.*mobility_tank.*?speed.*?(-?\d*\.?\d+)',"maxSpeed"),
                (r'.*mobility_tank.*?reverse.*?(-?\d*\.?\d+)',"reverseSpeed"),
                (r'.*mobility_tank.*?traverse.*?(-?\d*\.?\d+)',"traverseSpeed"),
                (r'.*mobility_tank.*?weight.*?(-?\d*\.?\d+)',"weight"),
                (r'.*mobility_tank.*?power.*?(-?\d*\.?\d+)',"enginePower"),
                (r'.*mobility_tank.*?track.*?(-?\d*\.?\d+)',"trackPerformance"),
                (r'.*mobility_tank.*?fuel.*?(-?\d*\.?\d+)',"fuelCapacity"),
                (r'.*mobility_tank.*?type.*?\((.*?)\)',"fuelType"),
                (r'.*gun_rot.*?speed2.*?(-?\d*\.?\d+)',"gunRotSpeed"),
                (r'.*inventory.*?\ apcbche.*?(-?\d*\.?\d+)',"apcbcheAmmo"),
                (r'.*inventory.*?\ he.*?(-?\d*\.?\d+)',"heAmmo"),
                (r'.*inventory.*?\ heat.*?(-?\d*\.?\d+)',"heatAmmo"),
                (r'.*inventory.*?\ aphebc.*?(-?\d*\.?\d+)',"aphebcAmmo"),
               ]
    for pattern, key in patterns:
        match = re.search(pattern, fileString, re.DOTALL)
        if match:
            dictionary[key].append(match.group(1))
        else:
            dictionary[key].append("N/A")

    dictionary["filePaths"].append(FirstfileName)
    dictionary['turretRotSpeed'].append(turretRotSpeed)
    dictionary["tankName"].append(entityName)

    return dictionary




    
def getTankData():

    dictionary = {"filePaths":[], "tankName":[], "turretRotSpeed":[], "maxSpeed":[], "reverseSpeed":[],
                  "traverseSpeed":[], "weight":[], "enginePower":[], "trackPerformance":[], "fuelCapacity":[],
                  "fuelType":[], "gunRotSpeed":[], "apcbcheAmmo":[], "heAmmo":[], "heatAmmo":[], "aphebcAmmo":[]
    };
    
    tankAndCannonFilePaths = getTankandCannonEntities()

    for tanks in tankAndCannonFilePaths:
        #print("hello")
        dictionary = getData(tanks, dictionary)
      
    return dictionary




def main():


    
  
    #print(getTankData())
    dataFrame = pd.DataFrame(getTankData())

   # print(os.getcwd())
    file_name = 'GoHStats.xlsx'
    dataFrame.to_excel(file_name)
    print('DataFrame has been written to Excel File successfully.')


main()    
exit()       










