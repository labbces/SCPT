import os
from Bio import SeqIO

# Parâmetros de entrada
input_file = "/Storage/data1/jorge.munoz/FILES_PANTRANSCRIPTOME/PanTranscriptome_2023.proteins"  
num_parts = 50  
output_prefix = "part"  
output_dir = "partes_proteinas"  

def split_fasta(input_file, num_parts):
    # Lê todas as sequências do arquivo FASTA
    sequences = list(SeqIO.parse(input_file, "fasta"))

    # Calcula quantas sequências devem ir em cada parte
    total_sequences = len(sequences)
    sequences_per_part = total_sequences // num_parts
    remainder = total_sequences % num_parts

    # Divide as sequências em partes
    parts = []
    start = 0
    for i in range(num_parts):
        end = start + sequences_per_part + (1 if i < remainder else 0)
        parts.append(sequences[start:end])
        start = end

    return parts

def write_fasta(parts, output_prefix, output_dir):
    for i, part in enumerate(parts):
        output_file = os.path.join(output_dir, f"{output_prefix}{i + 1}.fasta")
        with open(output_file, "w") as f:
            SeqIO.write(part, f, "fasta")
        print(f"Escreveu {len(part)} sequências para {output_file}")

# Divide o arquivo e escreve as partes
parts = split_fasta(input_file, num_parts)
write_fasta(parts, output_prefix, output_dir)
