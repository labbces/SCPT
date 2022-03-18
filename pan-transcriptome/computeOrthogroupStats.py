import argparse
import os

parser= argparse.ArgumentParser(description='compute stats from orthogroups.tsv')
parser.add_argument('--orthogroupsFile', metavar='orthogroupsFile', type=str, help='file with orthogroups generated with OrthoFinder2', required=True)
parser.add_argument('--numberSpecies', metavar='numberSpecies', type=int, help='Number of species', required=True)
args= parser.parse_args()

orthogroupsFile=args.orthogroupsFile
numberSpecies=args.numberSpecies
numberCoreOrthogroups=0
numberCoreProteins   =0
coreOrthogroups={}

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
                        # print(f'{fields[0]}\t{header[i]}\t{fields[i]}')
                if numberSpeciesInOrthogroup == numberSpecies:
                    numberCoreOrthogroups=numberCoreOrthogroups+1
                    # numberCoreProteins=numberCoreProteins+len(fields[1].split(','))
                    coreOrthogroups[fields[0]]=numberProteinsInOrthogroup
numberCoreProteins=sum(coreOrthogroups.values())
print(f'Number of groups present in all ({numberSpecies}) species:\t{numberCoreOrthogroups}\n')
print(f'Number of proteins present in core groups:\t{numberCoreProteins}\n')