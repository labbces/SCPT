import pandas as pd

df = pd.read_csv("OrthoFinder/SpeciesIDs.txt", sep=" ")
species_ids = pd.Series(df.index.values,index=df.specie)
#print(species_ids.to_dict)
print(species_ids[3])

'''
with open("OrthoFinder/head_B1.txt", "r+") as f:
  lines = f.readlines()
  f.seek(0)
  for index,line in enumerate(lines):
    print('0_' + str(index) + ': ' + line)
'''