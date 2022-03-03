### SCPT - SugarCane PanTranscriptome
### ! Under Construction !
### About
This repository contains a collection of scripts used to do the "Inference and functional annotation of the sugarcane pantranscriptome". Read more about the project: https://bv.fapesp.br/en/bolsas/190447/inference-and-annotation-of-the-sugarcane-pantranscriptome/

![Pan-Transcriptome](/images/CREATIVE.png)

This figure represents the almost complete collection of messenger RNA produced by a specie (Saccharum hybrid cultivar in this study). This collection can be called as pantranscriptome. The pantranscriptome of a specie can allow us to make coss-cultivar comparisons as well as to explore co-expression networks that will in turn aid in the functional annotation of until then transcripts of unknown function.

Contact information:

**Prof. Dr. Diego Mauricio Riaño-Pachón:** diego.riano@cena.usp.br  

**Felipe Vaz Peres:** felipe.vzps@gmail.com

### Data description
* **MyAssembly_Template**
  * Template used to assembly transcriptomes from their raw RNAseq datasets.
* **Scripts**
  * *extract_contaminants.py*: Script to extract and count the total reads of contaminant organisms based in the Kaiju report.
  * Snakefile: configuration file of our pipeline to semi-automatically generate sugarcane de novo transcriptome assemblies and remove possible genetic material from contaminant organisms in the reads. 


### Financial Support
This research has been supported by [São Paulo Research Foundation (FAPESP)](http://www.fapesp.br/en/), process number: [19/24796-5](https://bv.fapesp.br/en/bolsas/190447/inference-and-annotation-of-the-sugarcane-pantranscriptome/) and by 
Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq), process number: 310080/2018-5
