#!/Storage/progs/R-4.0.0/bin/R

#if (!require("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install()
#BiocManager::install("topGO")

#naming output
out = "Hard-core_classification_panTranscriptomeClassificationTable_I1.tsv"

#loading gene universe populated with GO terms
fname = "GO_universe_annotation_list"
go <- read.table(fname, quote='"', sep="\t", header=TRUE, colClasses = c('goid'='character', 'qpid'='character'))

interesting_fname ="classification_panTranscriptomeClassificationTable_I1.tsv"
interesting_table <- read.table(interesting_fname, sep="\t", header=TRUE, colClasses = c('classification'='character', 'gene_id'='character'))

#filtering ARGOT PPV score from Pannzer
go_filt <- go[ (go$ARGOT_PPV > 0.5),]
go_filt$goid <- paste0('GO:', go_filt$goid)

panzer_to_golist <- function(panzer_df){
  go_df <- aggregate( goid ~ qpid, data=panzer_df, FUN=c)
  structure(go_df$goid, .Names=go_df$qpid)
}

all_golist <- panzer_to_golist(go_filt)
#str(head(all_golist))

#Formatting the gene list
gene_names <- names(all_golist)

interesting_genes <- factor(as.integer(interesting_table$classification == "Hard-core"))
names(interesting_genes) <- gene_names

#interesting_genes
#all_golist

#Enrichment analysis
library(topGO)

#Creating topGOdata and running fischer's exact test
make_topGO_DO <- function(gene_list, ontology, gene2GO_list){
  topGO_data <- new("topGOdata", ontology = ontology, allGenes = gene_list,
                    annot = annFUN.gene2GO, gene2GO = gene2GO_list)
  fishers_result <- runTest(topGO_data, algorithm = "classic", statistic = "fisher")
  KS_result <- runTest(topGO_data, algorithm = "classic", statistic = "ks")
  KS_result.elim <- runTest(topGO_data, algorithm = "elim", statistic = "ks")
  allRes <- GenTable(topGO_data, classic = fishers_result, KS_result, KS_result.elim, ranksOf = "classic")
  
  #fishers_table <- GenTable(topGO_data, Fishers = fishers_result, useLevels = TRUE)
  allRes$Ontology <- ontology
  allRes
}

topGO_BP_table <- make_topGO_DO(interesting_genes, "BP", all_golist)
topGO_MF_table <- make_topGO_DO(interesting_genes, "MF", all_golist)
topGO_CC_table <- make_topGO_DO(interesting_genes, "CC", all_golist)

#topGO_BP_table

topGO_all_table <- (rbind(topGO_BP_table, topGO_MF_table, topGO_CC_table))
topGO_all_table

topGO_all_table <- topGO_all_table[order(topGO_all_table$classic),]
topGO_all_table

write.table(topGO_all_table, file = paste0(out, ".", ontology, ".csv"), sep =",", quote= F, col.names = T)

