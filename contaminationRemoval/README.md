### Removing contaminants from fastq files

### About 

We developed a simple method to remove unwanted sequences from raw fastq files, such as contaminating sequences.

### How does it work?

The [contamination removal software](https://github.com/labbces/SCPT/blob/master/contaminationRemoval/scripts/v4.remove_contaminants.py) removes contaminated sequences from fastq files based on the Taxonomy Level (NCBI Taxonomy) requested by the user and creates two output files: filtered.fastq and unclassified.fastq. See the flowchart below.

<img src="https://github.com/labbces/SCPT/blob/master/images/contaminationRemoval%20flowchart.png" alt="contamination flowchart" width="650"/>

To remove contaminated sequences, this software requires a Taxonomy Classification file and the fastq index as input. See the section Requirements to learn how to generate this files. 

### Running

With the Taxonomy Classification file and fastq index in hand, simply run the command below:
```
./v4.remove_contaminants.py -k $Taxonomy_Classification_file -R1 $R1.fastq -R2 $R2.fastq -t $Taxonomy Level
```
Where:
* -k = Taxonomy Classification file
* -R1 and -R2 = Paired fastq files
* -t = Taxonomy Level requested by the user. If Taxonomy Level = "Viridiplantae", only descendants from "Viridiplantae" will be maintained. 

Run `./v4.remove_contaminants.py --help` to read the help.

### Outputs

* `filtered.fastq files`: Sequences that have a taxonomic level within the Taxonomy Level requested by the user

* `unclassified.fastq files`: Sequences that didn't have an assigned taxonomic level

### Requirements

##### Kraken2 Database

Many software are used to generate a taxonomic classification file, such as [Kaiju](https://github.com/bioinformatics-centre/kaiju), [Kraken1](https://github.com/DerrickWood/kraken), [Kraken2](https://github.com/DerrickWood/kraken2). 

Here we used a custom Kraken2 database with the following available source databases: archaea, bacteria, fungi, human, nt, plant, protozoa, UniVec_Core and viral.

1. Install a taxonomy.
```
kraken2-build --download-taxonomy --db $DBNAME
```

2. Install reference libraries. 
```
kraken2-build --download-library archaea --db $DBNAME
kraken2-build --download-library bacteria --db $DBNAME
kraken2-build --download-library viral --db $DBNAME 
kraken2-build --download-library human --db $DBNAME 
kraken2-build --download-library fungi --db $DBNAME 
kraken2-build --download-library plant --db $DBNAME 
kraken2-build --download-library protozoa --db $DBNAME 
kraken2-build --download-library nt --db $DBNAME
```

3. Once your library is finalized, you need to build the database. 
```
kraken2-build --build --db $DBNAME
```
##### Running Kraken2

Once the library is built, it is time to generate the Taxonomy Classification file. This can be done with the command:
```
kraken2 --db $DBNAME --report-zero-counts --report $REPORT_OUTPUT --output $OUTPUT --paired $R1.fastq $R2.fastq
```
Where:
* --report-zero-counts = report taxa with no reads assigned
* --report = report how many reads in input data
* --output = report taxid assigned to each sequence 
* --paired = paired-end reads

##### Creating fastq 

To create a indexdb for your fastq files, simply run the command below:
```
./create_fastq_indexdb.py -R1 $R1.fastq -R2 $R2.fastq 
```

### Benchmarking
Comparison of RAM usage and Runtime between 4 versions of remove_contaminants.py script. 

<p float="left">
  <img src="https://github.com/labbces/SCPT/blob/master/images/RAM_usage.png" alt="RAM usage" width="470" />
  <img src="https://github.com/labbces/SCPT/blob/master/images/runtime.png" alt="Runtime" width="470" />
</p>  

The shorter runtime of versions 3 and 4 is due to the fact that these versions store the sequence id with its index, this process is performed with the biopython 'SeqIO.index' function.


