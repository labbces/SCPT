import shutil
from Bio import SeqIO
import os
import gzip
import argparse
import shutil
import re
import multiprocessing as mp


parser= argparse.ArgumentParser(description='compute pairwise identity for sets of orthogroups')
parser.add_argument('--orthogroupsFile', metavar='orthogroupsFile', type=str, help='file with orthogroups generated with OrthoFinder2', required=True)
parser.add_argument('--fastaFileGZ', dest='fastaFileGZ', type=str, help='Sequences in fasta format, compressed with gzip', required=True)
parser.add_argument('--nCPU', dest='nCPU', type=int, help='Number of cores to use', required=True)
args= parser.parse_args()

fastaFileGZ= args.fastaFileGZ
orthogroupsFile=args.orthogroupsFile
groupsDict={}

def getIdentity4cluster(clusterId):
    if os.path.isfile(clusterId+'.fasta'):
        if os.path.exists(clusterId+'.identity'):
            print('File '+clusterId+'.identity already exists, skipping')
        else:
            print(f'running identity for cluster {clusterId}')
            os.system('identity -d '+clusterId+'.fasta -o '+clusterId+'.identity -a y -c 2 -t 0 >/dev/null')
            if os.path.isfile(fields[0]+'.identity'):
                os.remove(clusterId+'.fasta')
    else:
        print('No fasta file for cluster '+clusterId)

if  shutil.which('identity'):
    print('Identity program found')
else:
    print('Identity program not found')
    exit()

if os.path.isfile(fastaFileGZ):
#    with gzip.open(fastaFileGZ, "rt") as fastaHandle:
#        fastaRecords = SeqIO.index(SeqIO.parse(fastaHandle, "fasta"),"fasta")
    fastaFile= re.sub('\.gz$', '', fastaFileGZ)
    if os.path.exists(fastaFile):
            print(f'uncompress sequence file present, using it . . .')
            fastaRecords = SeqIO.index_db("index_file.sqlite",fastaFile, "fasta")
    else:
        with gzip.open(fastaFileGZ, 'rb') as f_in:
            with open(fastaFile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)    
        #fastaRecords = SeqIO.index(fastaFile, "fasta")
        fastaRecords = SeqIO.index_db("index_file.sqlite",fastaFile, "fasta")
else:
    print("fasta file does not exist")
    exit()
    
if os.path.isfile(orthogroupsFile):
    with open(orthogroupsFile, "r") as file:
        for line in file:
            line=line.rstrip()
            if line.startswith('Group') or line.startswith('Orthogroup'):
                header=line.split('\t')
            else:
                fields=line.split('\t')
                for i in range(1,len(fields)):
                    transcripts=re.split(r', ?', fields[i])
                    for transcript in transcripts:
                        transcriptID=transcript.split(' ')[0]
                        # print(f'PPPPP {transcriptID} YYYYYYYYYYYYYYY {transcript} QQQQQ')
                        with open('pantranscriptome_groups.tsv', 'a') as outfile:
                            if transcriptID != '':
                                groupsDict[fields[0]]=1
                                outfile.write(f'{fields[0]}\t{header[i]}\t{transcriptID}\n')
                        if transcriptID in fastaRecords:
                            seqRecord=fastaRecords[transcriptID]
                            seqRecord.id=transcriptID
                            seqRecord.description=''
                            with open(fields[0]+'.fasta', 'a') as groupFastaFile:
                                SeqIO.write(seqRecord, groupFastaFile, "fasta")
                        else:
                            print(f'{transcriptID} not found in fasta file')

pool=mp.Pool(args.nCPU)
results=pool.map(getIdentity4cluster, groupsDict.keys())

with open('pairwiseIdentityPerGroup.tsv', 'w') as identityOutfile:
    for clusterID in groupsDict.keys():
        if os.path.exists(clusterID+'.identity'):
            with open(clusterID+'.identity', "r") as file:
                for line in file:
                    line=line.rstrip()
                    if not line.startswith('#'):
                        fieldsIdentity=line.split('\t')
                        # print(f'{fieldsIdentity}')
                        identityOutfile.write(f'{clusterID}\t{fieldsIdentity[0]}\t{fieldsIdentity[1]}\t{fieldsIdentity[2]}\n')
    # os.remove(fields[0]+'.identity')