#!/usr/bin/python

# Example command line : 
# > snakemake \
#   --snakefile dntap.py \
#   --configfile <config.yaml> \
#   --cores <max_n_cores>
# 
# To generate pipeline diagram: 
# > snakemake \
#   --snakefile dntap.py \
#   --configfile dntap_config.yaml \
#   --dag | dot -Tpng > diag1.png
#############

import os 

# Get current working directory  
dir_path = os.getcwd()
    
# User defined samples
SAMPLES = config["samples"] if config["samples"] is not None else []

# User defined ouput directory
OUT_DIR = config["directories"]["outdir"]

# Relative output directories
FASTQC_RAW_DIR = OUT_DIR + "fastqc_raw"
BBDUK_DIR = OUT_DIR + "bbduk_out/"
FASTQC_TRIMMED_DIR = OUT_DIR + "fastqc_trimmed"
KAIJU_DIR = OUT_DIR + "kaiju_out"
TRINITY_DIR = OUT_DIR + "trinity_out"
TRANSRATE_DIR = OUT_DIR + "transrate_out"
BUSCO_DIR = OUT_DIR + "busco_out"

# Software executable
fastqc = config["software"]["fastqc"]
bbduk = config["software"]["bbduk"]
kaiju = config["software"]["kaiju"]
trinity = config["software"]["trinity"]
transrate = config["software"]["transrate"]
busco = config["software"]["busco"]

# function to create fake inputs
def make_fake_inputs(index):
        
    if (index == "pe"): 
        
        sample_dir = os.path.dirname(SAMPLES["forward"])
        fake_file = sample_dir + "/none"
        os.system("touch " + fake_file)
        SAMPLES["single"] = fake_file
        
    elif (index == "se"): 
        
        sample_dir = os.path.dirname(SAMPLES["single"])
        fake_file = sample_dir + "/none"
        os.system("touch " + fake_file)
        SAMPLES["forward"] = fake_file
        SAMPLES["reverse"] = fake_file

# function to define inputs to RAW_FASTQC rule
def define_raw_fastqc_inputs(wildcards):
    data_type = config["data_type"]["type"]
    
    if (data_type == "pe"):
        input = [SAMPLES["forward"],SAMPLES["reverse"]]
        
    elif (data_type == "se"):
        input = SAMPLES["single"]
        
    return input

# creating fake files
make_fake_inputs(config["data_type"]["type"])

# ALL
rule all:
    input:
        fastqc_raw_out = FASTQC_RAW_DIR,            # FASTQC on raw FASTQ
        fastqc_trimmed_out = FASTQC_TRIMMED_DIR,    # FASTQC on filtered FASTQ
	kaiju_out = KAIJU_DIR,                      # Kaiju evidence of contamination
	transrate_out = TRANSRATE_DIR,              # assembly evaluation
	busco_out = BUSCO_DIR,                      # assembly evaluation


# FASTQC: This rule is use to generate an evaluation report raw FASTQ files 
# provided by the user.
rule raw_fastqc:
    input:
        fastq = define_raw_fastqc_inputs
    output:
        fastqc_raw_out = FASTQC_RAW_DIR
    log:
        OUT_DIR + "logs/fastqc/raw_fastqc.log"
    threads: 
        config["threads"]["fastqc"]
    shell:
        """
        mkdir {output.fastqc_raw_out}
        
        {fastqc} \
        -f fastq \
	-o {output.fastqc_raw_out} \
	{input.fastq} \
        --threads {threads} &> {log}
        """


# BBDUK: This rule is use to filter raw FASTQ files. 
rule bbduk:
    input:
        forward = SAMPLES["forward"],
        reverse = SAMPLES["reverse"],
        single = SAMPLES["single"]
    output:
        out = BBDUK_DIR
    log:
        OUT_DIR + "logs/bbduk/bbduk.log"
    threads: 
        config["threads"]["fastqc"]
    params:
        bbduk_params = config["bbduk_params"]
    run:
        if (config["data_type"]["type"] == "pe"):

            shell("""
            {bbduk} -Xmx40g \
            threads={threads} \
            in1={input.forward} \
            in2={input.reverse} \
            refstats= \ #Adicionar refstats - checar script BBduk
            stats= \ #Adicionar stats - checar script BBduk
            out1={output.out}forward.bbduk.fastq \
            out2={output.out}reverse.bbduk.fastq \
            {params.bbduk_params} 2> {log}
            """)

#FILTERED FASTQC: This rule is use to generate an evaluation report on 
# filtered FASTQ files previously processed by Trimmomatic.
rule trim_fastqc:
    input:
        BBDUK_DIR,
    output:
        fastqc_trimmed_out = FASTQC_TRIMMED_DIR
    log:
        OUT_DIR + "logs/fastqc/trimmed_fastqc.log"
    threads: 
        config["threads"]["fastqc"]
    run:
        if (config["data_type"]["type"] == "pe"):
            
            shell("""
            mkdir {output.fastqc_trimmed_out}
            
            {fastqc} \
            -f fastq
            -o {output.fastqc_trimmed_out}
            {input}/forward.bbduk.fastq \
            {input}/reverse.bbduk.fastq \
            --threads {threads} &> {log}
            """)

# KAIJU: asses evidence of contamination
rule kaiju:
#Adicionar parametros kaiju em "run".
    input:
        BBDUK_DIR,
    output:
        kaiju_out = KAIJU_DIR
    log:
        OUT_DIR + "logs/kaiju/kaiju.log"
    threads:
        config["threads"]["kaiju"]
    run:
        if (config["data_type"]["type"] == "pe"):

            shell("""
            mkdir {output.fastqc_trimmed_out}
            
            {fastqc} \
            {input}/forward.bbduk.fastq \
            {input}/reverse.bbduk.fastq \
            --outdir {output.fastqc_trimmed_out} \
            --threads {threads} &> {log}
            """)

# TRINITY: This rule is use to de novo assemble filtered FASTQ files into 
# contigs. 
rule trinity:
    input:
        BBDUK_DIR,
    output:
        trinity_out = TRINITY_DIR + "/Trinity.fasta"
    log:
        OUT_DIR + "logs/trinity/trinity.log"
    params:
        max_memory = config["trinity_params"]["max_memory"],
        trinity_dir = TRINITY_DIR
    threads: 
        config["threads"]["trinity"]
    run:
        if (config["data_type"]["type"] == "pe"):
            
            shell("""
            {trinity} \
            --seqType fq \
            --left {input}forward.bbduk.fastq \
            --right {input}reverse.bbduk.fastq \
            --output {params.trinity_dir} \
            --CPU {threads} \
            --SS_lib_type {params.lib_type} \
            --max_memory {params.max_memory} \
            --min_contig_length {params.min_contig_length} \
            --full_cleanup \
            --no_normalize_reads \
            --KMER_SIZE {params.KMER_SIZE} > {log}
            """)
            
# TRANSRATE: This rule is use to generate an evaluation report on previously
# de novo assembled contigs.
rule transrate:
    input:
        TRINITY_DIR + "/Trinity.fasta",
    output:
        transrate_out = TRANSRATE_DIR
    log:
        OUT_DIR + "logs/transrate/transrate.log"
    params:
        bbduk_dir = BBDUK_DIR
    threads: 
        config["threads"]["transrate"]
    run:
        if (config["data_type"]["type"] == "pe"):
            
            # Utilizar esta etapa para obter "Reads Metrics"
            # shell("""
            # {transrate} \
            # --assembly {input} \
            # --left {params.bbduk_dir}/forward.bbduk.fastq \
            # --right {params.bbduk_dir}/reverse.bbduk.fastq \
            # --output {output.transrate_out} \
            # --threads {threads} > {log}
            # """)

            shell("""
            {transrate} \
            --assembly {input} \
            --reference {params.reference} \
            --output {output.transrate_out} \
            --threads {threads} > {log}
            """)

rule busco:
    input:
        TRINITY_DIR + "/Trinity.fasta",
    output:
        busco_out = BUSCO_DIR
    log:
        OUT_DIR + "logs/busco/transrate.log"
    threads:
        config["threads"]["busco"]
    #params:
    #    busco_dir = BUSCO_DIR
    run:
        if (config["data_type"]["type"] == "pe"):

            shell("""
            {busco} \
            --i {input} \
            --output {output.busco_out} \
            --m {params.mode} \
            --l {params.database} \
            --threads {threads} > {log}
            """)

