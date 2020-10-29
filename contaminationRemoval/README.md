### About 

This directory contains 3 different versions of the 'remove contaminants.py' script.
The main function of this script is to remove sequences classified as contaminants from fastq files.

The contamination removal step can be detailed by the following flowchart:

![contamination_removal](/images/contamination_removal.png)

Different versions of this script have different structures and the runtime benchmarking is described below:

|      | v1        | v2        | v3        |
|------|-----------|-----------|-----------|
| real | 4m16.855s | 0m47.112s | 0m12.245s |
| user | 4m6.304s  | 0m39.913s | 0m9.743s  |
| sys  | 0m0.663s  | 0m0.537s  | 0m0.550s  |

The shorter runtime of version 3 is a consequence of storing the sequence id with its index, this process is performed with the biopython 'SeqIO.index' function.

In addition, version 3 writes the new filtered file while reading the raw fastq file. So only one line at time is stored in memory.

### Outputs

* R1 and R2 filtered.fastq files:

These files contains only sequences that have a taxonomic level within the taxonomic level entered by the user (e.g Viridiplantae) 

* R1 and R2 unclassified.fastq files:

Kaiju's unclassified sequences and sequences classified outside the taxonomic level entered by the user are included in these files (e.g every taxonomic level outside Viridiplantae)
