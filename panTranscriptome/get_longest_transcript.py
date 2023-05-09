#open a file in reading mode, and read a single line at the time
orthogroupsFile = '/home/diriano/Downloads/orthogroups_with_lengths.test.tsv'
longestTranscripot4Orthogroup='longestTranscripot4Orthogroup.tbl'

#use defaultdict library
from collections import defaultdict

longestTranscript=defaultdict(dict)

with open(orthogroupsFile, "r") as file:
    for line in file:
        line=line.rstrip()
        fields=line.split('\t')
        if fields[0] in longestTranscript.keys():
            #print(fields[0])
            currentKey=list(longestTranscript[fields[0]].keys())[0]
            #print(currentKey[0])
            if int(fields[2]) > int(list(longestTranscript[fields[0]].keys())[0]):
                del longestTranscript[fields[0]][currentKey]
                longestTranscript[fields[0]][fields[2]]=fields[1]
        else:
                longestTranscript[fields[0]][fields[2]]=fields[1]

for og in sorted(longestTranscript.keys()):
    for t in longestTranscript[og].keys():
        print(f'{og}\t{t}\t{longestTranscript[og][t]}')