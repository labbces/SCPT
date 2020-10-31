#!/usr/bin/env python

'''						Description
			This script counts the maximum number of lines that each splitted files
			needs to have. Each splitted file need to have multiple of 4 lines.
'''

import argparse
import os

# Creating arguments

parser = argparse.ArgumentParser(prog='count_lines_to_split_large_files.py', description='Count number of splitted files maximum lines', add_help=True)
parser.add_argument('-i', dest='large', metavar='<int>',type=int, help='Total lines of large file', required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')

# Getting arguments

args = parser.parse_args()
large = args.large

# Calculate

divisor = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

for i in divisor:
	calc = large/i
	if calc % 4==0:
		lines = large/i
		sequences = lines/4
		print("Number of lines if you want {} files = {} lines. Number of sequences in this file = {} sequences.".format(i, lines, sequences))
