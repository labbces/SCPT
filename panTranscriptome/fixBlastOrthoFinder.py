from fileinput import filename
from genericpath import exists
import gzip
import glob
import argparse
import re
import os.path
import os

parser= argparse.ArgumentParser(description='fix blast results, worng species order')
parser.add_argument('--dir', type=str, help='file with blast results', required=True)
args= parser.parse_args()

files2change={}

# open a gzipped file for reading: 
pathBlastFiles=args.dir+'/Blast*.txt.gz'
for file in glob.glob(pathBlastFiles):
    basename = os.path.basename(file)
    sp1,sp2=basename.split('.')[0].split('_')
    sp1=re.sub('Blast','',sp1)
    # print(f'{sp1}\t{sp2}')
    if sp1 != sp2:
        if basename not in files2change.keys():
            print(basename)
            with gzip.open(file, 'rt') as f:
                content = f.readlines()
                fields=content[0].split('\t')
                regex1=r"^"+sp2+r"_"
                regex2=r"^"+sp1+r"_"
                if re.match(regex1,fields[0]) and re.match(regex2,fields[1]):
                    secondfile='Blast'+sp2+'_'+sp1+'.txt.gz'
                    if secondfile not in files2change.keys():
                        files2change[secondfile]=basename


for file in files2change.keys():
    print(f'{file}\t{files2change[file]}')
    sp1,sp2=file.split('.')[0].split('_')
    sp1=re.sub('Blast','',sp1)
    # print(f'{args.dir} {file}')
    tmpName=sp2+'_'+sp1
    old_fileA = os.path.join(args.dir, file)
    new_fileA = os.path.join(args.dir, tmpName)
    old_fileB = os.path.join(args.dir, files2change[file])
    new_fileB = os.path.join(args.dir, file)
    print(f'\t{old_fileA} {new_fileA}\n\t{old_fileB} {new_fileB}\n\t{new_fileA} {old_fileB}\t')
    if (exists(old_fileA) and exists(old_fileB)):
        os.rename(old_fileA, new_fileA)
        os.rename(old_fileB, new_fileB)
        os.rename(new_fileA, old_fileB)
    else:
        print(f'missing files check {old_fileA} {old_fileB}')