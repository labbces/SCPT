#if (!require("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install()
#BiocManager::install("topGO")

#naming output
out = "Accessory_classification_panTranscriptomeClassificationTable_I1.tsv"

#loading gene universe populated with GO terms
#add headers: classification gene_id

fname = "GO_universe_annotation_list"
go <- read.table(fname, quote='"', sep="\t", header=TRUE, colClasses = c('goid'='character', 'qpid'='character'))

interesting_fname ="classification_panTranscriptomeClassificationTable_I1.tsv"
interesting_table <- read.table(interesting_fname, sep="\t", header=TRUE, colClasses = c('classification'='character', 'gene_id'='character'))

#filtering ARGOT PPV score from Pannzer
go_filt <- go[ (go$ARGOT_PPV > 0),]
go_filt$goid <- paste0('GO:', go_filt$goid)

panzer_to_golist <- function(panzer_df){
  go_df <- aggregate( goid ~ qpid, data=panzer_df, FUN=c)
  structure(go_df$goid, .Names=go_df$qpid)
}

all_golist <- panzer_to_golist(go_filt)
#str(head(all_golist))

#Formatting the gene list
gene_names <- names(all_golist)

interesting_genes <- factor(as.integer(interesting_table$classification == "Accessory"))
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
  #KS_result <- runTest(topGO_data, algorithm = "classic", statistic = "ks")
  #KS_result.elim <- runTest(topGO_data, algorithm = "elim", statistic = "ks")
  #allRes <- GenTable(topGO_data, classic = fishers_result, KS_result, KS_result.elim, ranksOf = "classic")
  allRes <- GenTable(topGO_data, classic = fishers_result, ranksOf = "classic", topNodes=30)
  
  #fishers_table <- GenTable(topGO_data, Fishers = fishers_result, useLevels = TRUE)
  allRes$Ontology <- ontology
  allRes$classic <- as.numeric(allRes$classic)
  allRes <- allRes[c("GO.ID","Term","classic")]
  allRes
}

topGO_BP_table <- make_topGO_DO(interesting_genes, "BP", all_golist)
#topGO_MF_table <- make_topGO_DO(interesting_genes, "MF", all_golist)
#topGO_CC_table <- make_topGO_DO(interesting_genes, "CC", all_golist)

#topGO_BP_table

#topGO_all_table <- (rbind(topGO_BP_table, topGO_MF_table, topGO_CC_table))
#topGO_all_table

#topGO_all_table <- topGO_all_table[order(topGO_all_table$classic),]
topGO_all_table <- topGO_BP_table[order(topGO_BP_table$classic),]
topGO_all_table

#write.table(topGO_all_table, file = paste0(out, ".BP", ".csv"), sep =",", quote= F, col.names = T)
#install.packages("ggplot2")
library(ggplot2)

ntop <- 30
ggdata <- topGO_all_table[1:ntop,]
ggdata$Term <- factor(ggdata$Term, levels = rev(ggdata$Term)) # fixes order
ggplot(ggdata,
       aes(x = Term, y = -log10(classic), size = -log10(classic), fill = -log10(classic))) +
  
  expand_limits(y = 1) +
  geom_point(shape = 21) +
  scale_size(range = c(2.5,12.5)) +
  scale_fill_continuous(low = 'royalblue', high = 'red4') +
  
  xlab('') + ylab('Enrichment score') +
  labs(
    title = 'GO Analysis',
    #subtitle = 'Top 50 terms ordered by Kolmogorov-Smirnov p-value',
    subtitle = 'Top 30 terms ordered by Fisher Exact p-value',
    caption = 'Cut-off lines drawn at equivalents of p=0.05, p=0.01, p=0.001') +
  
  geom_hline(yintercept = c(-log10(0.05), -log10(0.01), -log10(0.001)),
             linetype = c("dotted", "longdash", "solid"),
             colour = c("black", "black", "black"),
             size = c(0.5, 1.5, 3)) +
  
  theme_bw(base_size = 24) +
  theme(
    legend.position = 'right',
    legend.background = element_rect(),
    plot.title = element_text(angle = 0, size = 16, face = 'bold', vjust = 1),
    plot.subtitle = element_text(angle = 0, size = 14, face = 'bold', vjust = 1),
    plot.caption = element_text(angle = 0, size = 12, face = 'bold', vjust = 1),
    
    axis.text.x = element_text(angle = 0, size = 12, face = 'bold', hjust = 1.10),
    axis.text.y = element_text(angle = 0, size = 12, face = 'bold', vjust = 0.5),
    axis.title = element_text(size = 12, face = 'bold'),
    axis.title.x = element_text(size = 12, face = 'bold'),
    axis.title.y = element_text(size = 12, face = 'bold'),
    axis.line = element_line(colour = 'black'),
    
    #Legend
    legend.key = element_blank(), # removes the border
    legend.key.size = unit(1, "cm"), # Sets overall area/size of the legend
    legend.text = element_text(size = 14, face = "bold"), # Text size
    title = element_text(size = 14, face = "bold")) +
  
  coord_flip()
ggplot2::ggsave("Accessory_GOTerms_P30_Cortex_Fisher.pdf",
                device = NULL,
                height = 8.5,
                width = 12)

