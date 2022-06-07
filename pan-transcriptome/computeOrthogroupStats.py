import argparse
import os
from re import S
import pandas as pd


parser= argparse.ArgumentParser(description='compute stats from orthogroups.tsv')
parser.add_argument('--orthogroupsFile', metavar='orthogroupsFile', type=str, help='file with orthogroups generated with OrthoFinder2', required=True)
parser.add_argument('--numberSpecies', metavar='numberSpecies', type=int, help='Number of species', required=True)
args= parser.parse_args()

orthogroupsFile=args.orthogroupsFile
numberSpecies=args.numberSpecies
numberCoreOrthogroups=0
numberCoreProteins   =0
coreOrthogroups={}
numberProreinsPerGroup={}
numberProreinsPerGroupPerSpecies={}
proteinPerOrthogroup={}
proteinPerOrthogroup['core']={}
proteinPerOrthogroup['noncore']={}
exclusiveGroups={}
exclusiveGenes={}

if os.path.isfile(orthogroupsFile):
    with open(orthogroupsFile, "r") as file:
        for line in file:
            line=line.rstrip()
            if line.startswith('Orthogroup'):
                header=line.split('\t')
            else:
                numberSpeciesInOrthogroup=0
                numberProteinsInOrthogroup=0
                fields=line.split('\t')
                for i in range(1,len(fields)):
                    if fields[i] != '':
                        numberSpeciesInOrthogroup=numberSpeciesInOrthogroup+1
                        numberProteinsInOrthogroup=numberProteinsInOrthogroup+len(fields[i].split(','))
                        numberProreinsPerGroup[fields[0]]=numberProteinsInOrthogroup
                        if fields[0] not in numberProreinsPerGroupPerSpecies.keys():
                            numberProreinsPerGroupPerSpecies[fields[0]]={}
                            numberProreinsPerGroupPerSpecies[fields[0]][header[i]]=len(fields[i].split(','))
                        else:
                            numberProreinsPerGroupPerSpecies[fields[0]][header[i]]=len(fields[i].split(','))
                            # print(f'{fields[0]}\t{header[i]}\t{numberProreinsPerGroupPerSpecies[fields[0]][header[i]]}')
                        # print(f'{fields[0]}\t{header[i]}\t{fields[i]}')
                if numberSpeciesInOrthogroup == numberSpecies:
                    numberCoreOrthogroups=numberCoreOrthogroups+1
                    # numberCoreProteins=numberCoreProteins+len(fields[1].split(','))
                    coreOrthogroups[fields[0]]=numberProteinsInOrthogroup
                    numberProteinsInOrthogroupPerSpecies=0
                    for sp in numberProreinsPerGroupPerSpecies[fields[0]].keys():
                        if fields[0] not in proteinPerOrthogroup['core'].keys():
                            proteinPerOrthogroup['core'][fields[0]]={}
                            if sp not in proteinPerOrthogroup['core'][fields[0]].keys():
                                proteinPerOrthogroup['core'][fields[0]][sp]=numberProreinsPerGroupPerSpecies[fields[0]][sp]
                        else:
                            if sp not in proteinPerOrthogroup['core'][fields[0]].keys():
                                proteinPerOrthogroup['core'][fields[0]][sp]=numberProreinsPerGroupPerSpecies[fields[0]][sp]
                else:
                    for sp in numberProreinsPerGroupPerSpecies[fields[0]].keys():
                        if fields[0] not in proteinPerOrthogroup['core'].keys():
                            proteinPerOrthogroup['noncore'][fields[0]]={}
                            if sp not in proteinPerOrthogroup['noncore'][fields[0]].keys():
                                proteinPerOrthogroup['noncore'][fields[0]][sp]=numberProreinsPerGroupPerSpecies[fields[0]][sp]
                                # print(f'noncore {fields[0]} {sp} {numberProreinsPerGroupPerSpecies[fields[0]][sp]}')
                        else:
                            if sp not in proteinPerOrthogroup['noncore'][fields[0]].keys():
                                proteinPerOrthogroup['noncore'][fields[0]][sp]=numberProreinsPerGroupPerSpecies[fields[0]][sp]
                if numberSpeciesInOrthogroup == 1:
                    # print(f'{list(numberProreinsPerGroupPerSpecies[fields[0]].keys())}')
                    for sp in numberProreinsPerGroupPerSpecies[fields[0]].keys():
                        if sp in exclusiveGroups.keys():
                            exclusiveGroups[sp]=exclusiveGroups[sp]+1
                            exclusiveGenes[sp] =exclusiveGenes[sp]+numberProreinsPerGroupPerSpecies[fields[0]][sp]
                        else:
                            exclusiveGroups[sp]=1
                            exclusiveGenes[sp] =numberProreinsPerGroupPerSpecies[fields[0]][sp]
                    # print(exclusiveGroups[sp])
                    # print(fields[0])

# for t in proteinPerOrthogroup.keys():
#     for og in proteinPerOrthogroup[t].keys():
#         for sp in proteinPerOrthogroup[t][og].keys():
#             print(f'{t}\t{og}\t{sp}\t{proteinPerOrthogroup[t][og][sp]}', file=open('orthogousNumbProts.txt', 'a'))

for sp in exclusiveGroups.keys():
    print(f'{sp}\t{exclusiveGroups[sp]}\t{exclusiveGenes[sp]}')

numberCoreProteins=sum(coreOrthogroups.values())
averageNumberOfProtesPerOrthogroupInCore=numberCoreProteins/numberCoreOrthogroups
averageNumberOfProtesPerOrthogroupInCorePerspecies=0
print(f'Number of groups present in all ({numberSpecies}) species:\t{numberCoreOrthogroups}\n')
print(f'Number of proteins present in core groups:\t{numberCoreProteins}\n')
print(f'Average number of proteins present in core groups:\t{averageNumberOfProtesPerOrthogroupInCore}\n')