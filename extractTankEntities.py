import os
import pandas as pd
import re
import tkinter as tk
from tkinter import simpledialog


def getTankEntities(directory):
    turretedArrayFilePaths = []
    for root,d_names,f_names in os.walk(directory):
            if re.search(r'.*tank((?!x).)*$', root):
                for file in f_names:
                    if file.endswith(".def"):
                        filePath = os.path.join(root, file)
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
    #this array is consists of a regex and a key pair, the key must be as spelt the same as the corresponding key in the getTankData method
    #the order of the array isnt important 
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
    #this adds the extracted values to the correct key in the dictionary 
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



 
def getTankData(directory):
    #dictionary containing all value keys for the tank entity 
    dictionary = {"filePaths":[], "tankName":[], "turretRotSpeed":[], "maxSpeed":[], "reverseSpeed":[],
                  "traverseSpeed":[], "weight":[], "enginePower":[], "trackPerformance":[], "fuelCapacity":[],
                  "fuelType":[], "gunRotSpeed":[], "apcbcheAmmo":[], "heAmmo":[], "heatAmmo":[], "aphebcAmmo":[]
                  };
    #this retrieves the relevant file paths
    tankAndCannonFilePaths = getTankEntities(directory)
    #retrieves all other tank entity information
    for tanks in tankAndCannonFilePaths:
        dictionary = getData(tanks, dictionary)
    return dictionary




def interface():
    ROOT = tk.Tk()
    ROOT.withdraw()
   # the input dialog
    USER_INP = simpledialog.askstring(title="Input",
            prompt="Input mod name as is written in its GoH directory")
    # check it 
    return USER_INP
    



def main():
    modName = interface()
    game_dir = f'Steam/steamapps/common/Call to Arms - Gates of Hell/mods/{modName}'

    try:
       os.chdir(os.path.join(os.environ.get("ProgramFiles(X86)"), game_dir))
    except FileNotFoundError:
       print("Directory not found.")
       exit()
    except Exception as e:
       print("An error occurred:", e)
       exit()


    data_frame = pd.DataFrame(getTankData("./resource/entity/-vehicle"))
    data_frame.to_csv('GoHTanks.csv', index=False)
    print('DataFrame has been written to Excel File successfully.')
   
     

if __name__ == "__main__":
    main()







