#!/usr/bin/env python

'''                 Description
    Extract taxon and clade names by the percentage
    of fragments covered by the clade in a taxon. 
'''

import argparse

parser = argparse.ArgumentParser(prog='extract_clades.py', description='Extract taxon and clade names by the percentage of fragments covered by the clade in a taxon', add_help=True)
parser.add_argument('-i', dest='input_kraken', metavar='<kraken report file>', required=True)
parser.add_argument('-r', dest='reads', metavar='<int>', type=int,  required=True)
#parser.add_argument('-p', dest='percentage', metavar='<0 to 100>', type=int,  required=True)

args = parser.parse_args()
input_kraken = args.input_kraken
reads = args.reads
#percentage = args.percentage

with open(input_kraken, "r") as kraken, open(input_kraken + "_extracted_clade.csv", "w") as output:
    for line in kraken.readlines():
        #if float(line.split()[0]) >= percentage:
        if int(line.split()[2]) >= reads:
            output.write(line)

    
