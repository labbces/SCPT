import shutil
from Bio import SeqIO
import os
import gzip
import argparse
import shutil
import re

parser= argparse.ArgumentParser(description='compute pairwise identity for sets of orthogroups')
parser.add_argument('--orthogroupsFile', metavar='orthogroupsFile', type=str, help='file with orthogroups generated with OrthoFinder2', required=True)
parser.add_argument('--fastaFileGZ', dest='fastaFileGZ', type=str, help='Sequences in fasta format, compressed with gzip', required=True)
args= parser.parse_args()

fastaFileGZ= args.fastaFileGZ
orthogroupsFile=args.orthogroupsFile
groupsDict={}

if  shutil.which('identity'):
    print('Identity program found')
else:
    print('Identity program not found')
    exit()

if os.path.isfile(fastaFileGZ):
#    with gzip.open(fastaFileGZ, "rt") as fastaHandle:
#        fastaRecords = SeqIO.index(SeqIO.parse(fastaHandle, "fasta"),"fasta")
    fastaFile= re.sub('\.gz$', '', fastaFileGZ)
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
            if line.startswith('Group'):
                header=line.split('\t')
            else:
                fields=line.split('\t')
                for i in range(1,len(fields)):
                    transcripts=fields[i].split(', ?')
                    for transcript in transcripts:
                        transcriptID=transcript.split(' ')[0]
                        with open('pantranscriptome_groups.tsv', 'a') as outfile:
                            if transcriptID != '':
                                outfile.write(f'{fields[0]}\t{header[i]}\t{transcriptID}\n')
                        if transcriptID in fastaRecords:
                            seqRecord=fastaRecords[transcriptID]
                            seqRecord.id=transcriptID
                            seqRecord.description=''
                            with open(fields[0]+'.fasta', 'a') as groupFastaFile:
                                SeqIO.write(seqRecord, groupFastaFile, "fasta")
                        else:
                            print(f'{transcriptID} not found in fasta file')
                if os.path.isfile(fields[0]+'.fasta'):
                    os.system('identity -d '+fields[0]+'.fasta -o '+fields[0]+'.identity -a y -c 3 -t 0')
                    os.remove(fields[0]+'.fasta')
                    if os.path.isfile(fields[0]+'.identity'):
                        with open(fields[0]+'.identity', "r") as file:
                            for line in file:
                                line=line.rstrip()
                                if not line.startswith('#'):
                                    fieldsIdentity=line.split('\t')
                                    with open('pairwiseIdentityPerGroup.tsv', 'a') as identityOutfile:
                                        identityOutfile.write(f'{fields[0]}\t{fieldsIdentity[0]}\t{fieldsIdentity[1]}\t{fieldsIdentity[2]}\n')
                        os.remove(fields[0]+'.identity')