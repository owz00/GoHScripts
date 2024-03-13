from PyPAKParser import PakParser
import os
import pandas as pd
import re


def getBreeds(directory):
    breedFilePaths = []
    for root,d_names,f_names in os.walk(directory):
                    for files in f_names:
                        if files.endswith(".set"):
                            filePath = os.path.join(root, files)
                            breedFilePaths.append(filePath)
    return breedFilePaths



def getData(FirstfileName, dictionary):
    fileString = ""
     
    match = re.search(r'(\w*)\.set?', FirstfileName)
    entityName = match.group(1)
   
    with open(FirstfileName) as file:
        #add all lines of the text file to a string
        lines = file.readlines()
        for line in lines:
              fileString += line
              
   
    #this array is consists of a regex and a key pair, the key must be as spelt the same as the corresponding key in the getTankData method
    #the order of the array isnt important 
    patterns = [(r'.*veterancy_lvl_(-?\d*\.?\d+)', "Veterancy"),
                (r'rifle_skill_rank_(-?\d*\.?\d+)', "Rifle Skill"),
                (r'smg_skill_rank_(-?\d*\.?\d+)', "Smg Skill"),
                (r'at_rank_(-?\d*\.?\d+)', "At Skill"),
                (r'loader_skill_rank_(-?\d*\.?\d+)', "Loader Skill"),
                (r'mg_skill_rank_(-?\d*\.?\d+)', "Mg Skill"),
                (r'loader_skill_smg_rank_(-?\d*\.?\d+)', "Smg Loader Skill"),
          
                ]
    #this adds the extracted values to the correct key in the dictionary 
    for pattern, key in patterns:
        match = re.search(pattern, fileString, re.DOTALL)
        if match:
            dictionary[key].append(match.group(1))
        else:
           dictionary[key].append("N/A")

    dictionary["filePath"].append(FirstfileName)
    dictionary["breedName"].append(entityName)

    return dictionary



 
def getBreedData(directory):
    #dictionary containing all value keys for the tank entity 
    dictionary = {"filePath":[], "breedName":[],"Veterancy":[], "Rifle Skill":[], "Smg Skill":[], "At Skill":[], "Loader Skill":[],
                  "Mg Skill":[], "Smg Loader Skill":[]};
    #this retrieves the relevant file paths
    breedFilePaths = getBreeds(directory)
    #retrieves all other tank entity information
    for breeds in breedFilePaths:
        dictionary = getData(breeds, dictionary)
    return dictionary




def main():
    game_dir = 'Steam/steamapps/common/Call to Arms - Gates of Hell/mods/template'
    os.chdir(os.path.join(os.environ.get("ProgramFiles(X86)"), game_dir))
    #print(getBreeds("./resource/gamelogic/set/breed/mp"))
    data_frame = pd.DataFrame(getBreedData("./resource/gamelogic/set/breed/mp"))
    file_name = 'GoHBreeds.xlsx'
    data_frame.to_excel(file_name)
    print('DataFrame has been written to Excel File successfully.')
   
     

if __name__ == "__main__":
    main()







