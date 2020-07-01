### About
This script extract and count the total reads of contaminant organisms based in the Kaiju report. 

[Kaiju](http://kaiju.binf.ku.dk/) do a fast and sensitive taxonomic classification for metagenomics datasets, and here we are using Kaiju to predict contamination in the raw RNAseq datasets from Sugarcane studies.

### Kaiju report example:
```
less SRR5258946.kaiju_speciesSummary.tsv
```
![Kaiju_example](/images/kaiju_example.png)
 
### extract_contaminants.py usage
* Kaiju generates one report for each Accession (RNAseq accession from [Sequence Read Archive from NCBI](https://www.ncbi.nlm.nih.gov/sra)), so the first step is to merge all kaiju reports into one file:

  * (We only want the taxonomic classification of the organisms with presence higher than 1% in the dataset, to do that, we can merge only the first lines of the report)

```
head *.tsv > raw_summary.tsv
```
* Now we can run *extract_contaminants.py* to get the taxonomic classification and the total reads of the organisms based in a percentage threshold:
```
extract_contaminants.py -i raw_summary.tsv -p 1 -o raw_kaijuClassification
```

### Usage manual:
```
extract_contaminants.py --help
```
![extract_contaminantsHelp](/images/extract_contaminantsHelp.png)
