### Removing contaminants from fastq files
### ! Under Construction !
### About 
This directory contains 3 different versions of the 'remove contaminants.py' script.
The main function of this script is to remove sequences classified as contaminants from fastq files.

The contamination removal step can be detailed by the following flowchart:

![contamination_removal](/images/contamination_removal.png)

### Usage
The taxid file can be generated using Kaiju or Kraken. 
We used a custom Kraken database with the following available source databases: archaea, bacteria, fungi, human, nt, plant, protozoa, UniVec_Core and viral 

1. Split large kaiju file into pieces running `submit_slit_large_kaiju_file.sh`
2. Generate an index_db for the fastq files running `create_fastq_indexdb.py`
3. And then, run `v4.remove_contaminants.py`

### Outputs

* `R1 and R2 filtered.fastq files`: Contains only sequences that have a taxonomic level within the taxonomic level entered by the user (e.g Viridiplantae) 

* `R1 and R2 unclassified.fastq files`: Kaiju's unclassified sequences and sequences classified outside the taxonomic level entered by the user (e.g every taxonomic level outside Viridiplantae)

### Validation
You can validate your filtered files running Kaiju or Kraken against the database used to generate the labeled file. If everything worked well, you will only see reads with taxonomic level within the taxonomic level inserted by the user (Viridiplantae in this study).   

OBS: If you are using Kraken, you have to merge all filtered.fastq files with the simply following command:
```
cat *filtered.R1* > $prefix.filtered.R1.fastq
cat *filtered.R2* > $prefix.filtered.R1.fastq
cat *unclassified.R1* > $prefix.unclassified.R1.fastq
cat *unclassified.R1* > $prefix.unclassified.R2.fastq
```
This prevents Kraken from using unnecessary RAM, as for each round the kraken loads the complete hash table dataset (254GB in this study). 

### Benchmarking
Comparison of runtime and RAM usage between 4 versions of remove_contaminants.py script. 

![runtime](/images/runtime.png)

![RAM_usage](/images/RAM_usage.png)

The shorter runtime of versions 3 and 4 is due to the fact that these versions store the sequence id with its index, this process is performed with the biopython 'SeqIO.index' function.

In addition, version 3 and 4 writes the new filtered file while reading the raw fastq file. So only one line at time is stored in memory.


