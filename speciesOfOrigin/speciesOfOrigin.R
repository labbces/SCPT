library(tximport)
library(reshape2)
library(ggplot2)
setwd("C:/Users/Avell 5/Downloads/Verusca//")
rm(list=ls())

countsOrigin<-read.delim(file = "Salmon.joint.txt",header=T,row.names=1)
head(countsOrigin)
colnames(countsOrigin)<-c('S._barberi','S._officinarum','S._spontaneum')
origNumberGenes=dim(countsOrigin)[1]
dim(countsOrigin)
head(countsOrigin)
table(rowSums(countsOrigin)==0)
countsOrigin<-countsOrigin[!rowSums(countsOrigin)==0,] #remove transcript without reads mapped in both sps
countsOrigin$CPM_SOFF<-((countsOrigin[,'S._officinarum']+0.1)*10e6)/(sum(countsOrigin[,'S._officinarum']))
countsOrigin$CPM_SSPO<-((countsOrigin[,'S._spontaneum']+0.1)*10e6)/(sum(countsOrigin[,'S._spontaneum']))
countsOrigin$CPM_SBAR<-((countsOrigin[,'S._barberi']+0.1)*10e6)/(sum(countsOrigin[,'S._barberi']))
countsOrigin$ratioCPM_SSPO_vs_SOFF<-countsOrigin$CPM_SSPO/countsOrigin$CPM_SOFF
countsOrigin$log10ratioCPM_SSPO_vs_SOFF<-round(log10(countsOrigin$CPM_SSPO/countsOrigin$CPM_SOFF),2)
countsOrigin$ratioCPM_SSPO_vs_SBAR<-countsOrigin$CPM_SSPO/countsOrigin$CPM_SBAR
countsOrigin$log10ratioCPM_SSPO_vs_SBAR<-round(log10(countsOrigin$CPM_SSPO/countsOrigin$CPM_SBAR),2)
countsOrigin$ratioCPM_SOFF_vs_SBAR<-countsOrigin$CPM_SOFF/countsOrigin$CPM_SBAR
countsOrigin$log10ratioCPM_SOFF_vs_SBAR<-round(log10(countsOrigin$CPM_SOFF/countsOrigin$CPM_SBAR),2)
countsOrigin$Fraction_SSPO<-round(countsOrigin$CPM_SSPO/(countsOrigin$CPM_SOFF+countsOrigin$CPM_SSPO+countsOrigin$CPM_SBAR),3)
countsOrigin$Fraction_SOFF<-round(countsOrigin$CPM_SOFF/(countsOrigin$CPM_SOFF+countsOrigin$CPM_SSPO+countsOrigin$CPM_SBAR),3)
countsOrigin$Fraction_SBAR<-round(countsOrigin$CPM_SBAR/(countsOrigin$CPM_SOFF+countsOrigin$CPM_SSPO+countsOrigin$CPM_SBAR),3)
head(countsOrigin)

countsOrigin[which(countsOrigin$Fraction_SBAR >0.7),]
countsOrigin$Origin<-NA
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & abs(countsOrigin$log10ratioCPM_SSPO_vs_SOFF) < 1 & abs(countsOrigin$log10ratioCPM_SOFF_vs_SBAR) < 1 & abs(countsOrigin$log10ratioCPM_SSPO_vs_SBAR) < 1),]),'Origin']<-'Common'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$log10ratioCPM_SSPO_vs_SOFF >= 1 & abs(countsOrigin$log10ratioCPM_SOFF_vs_SBAR) < 1 & countsOrigin$log10ratioCPM_SSPO_vs_SBAR >= 1),]),'Origin']<-'SSPO'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$log10ratioCPM_SSPO_vs_SOFF <= -1 & countsOrigin$log10ratioCPM_SOFF_vs_SBAR >= 1 & abs(countsOrigin$log10ratioCPM_SSPO_vs_SBAR) < 1),]),'Origin']<-'SOFF'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & abs(countsOrigin$log10ratioCPM_SSPO_vs_SOFF) < 1 & countsOrigin$log10ratioCPM_SOFF_vs_SBAR <= -1 & countsOrigin$log10ratioCPM_SSPO_vs_SBAR <= -1),]),'Origin']<-'SBAR'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._officinarum == 0 & countsOrigin$log10ratioCPM_SSPO_vs_SBAR <= -1),]),'Origin']<-'SBAR'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._officinarum == 0 & countsOrigin$log10ratioCPM_SSPO_vs_SBAR >= 1),]),'Origin']<-'SSPO'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._officinarum == 0 & abs(countsOrigin$log10ratioCPM_SSPO_vs_SBAR) < 1),]),'Origin']<-'CommonSSPO_SBAR'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._spontaneum == 0 & countsOrigin$log10ratioCPM_SOFF_vs_SBAR <= -1),]),'Origin']<-'SBAR'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._spontaneum == 0 & countsOrigin$log10ratioCPM_SOFF_vs_SBAR >= 1),]),'Origin']<-'SOFF'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._spontaneum == 0 & abs(countsOrigin$log10ratioCPM_SOFF_vs_SBAR) < 1),]),'Origin']<-'CommonSOFF_SBAR'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._barberi == 0 & countsOrigin$log10ratioCPM_SSPO_vs_SOFF <= -1),]),'Origin']<-'SOFF'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._barberi == 0 & countsOrigin$log10ratioCPM_SSPO_vs_SOFF >= 1),]),'Origin']<-'SSPO'
countsOrigin[rownames(countsOrigin[which(is.na(countsOrigin$Origin) & countsOrigin$S._barberi == 0 & abs(countsOrigin$log10ratioCPM_SSPO_vs_SOFF) <= 1),]),'Origin']<-'CommonSSPO_SOFF'

#countsOrigin[which(is.na(countsOrigin$Origin)),]
countsOrigin['evm.model.uti_cns_0018261.2',]
table(countsOrigin$Origin, useNA = 'always')

ggplot(as.data.frame(countsOrigin),aes(x=Fraction_SBAR)) +
  theme_bw()+
  geom_histogram(bins=1000)+
  scale_x_log10()
  
  
ggplot(as.data.frame(countsOrigin),aes(x=ratioCPM)) +
  theme_bw()+
  geom_histogram(bins=1000)+
  scale_x_log10()+
  geom_vline(xintercept = 1,color='red')

ggplot(as.data.frame(countsOrigin),aes(x=log10ratioCPM)) +
  theme_bw()+
  geom_histogram(bins=1000)+
  geom_vline(xintercept = 0,color='red')+
  geom_vline(xintercept = -1,color='blue')+
  geom_vline(xintercept = 1,color='blue')+
  xlab('ratio of CPM, log10 scale')+
  ylab('Number of transcripts')

ggplot(as.data.frame(countsOrigin),aes(x=CPM_SOFF, y=CPM_SSPO)) +
  theme_bw()+
  geom_jitter()+
  xlab('Log10 CPM S. spontaneum')+
  ylab('Log10 CPM S. officinarum')+
  scale_x_log10()+
  scale_y_log10()

dim(countsOrigin[which(countsOrigin$log10ratioCPM>-1 & countsOrigin$log10ratioCPM<1),]) #possible recombinants, or common to both species
dim(countsOrigin[which(countsOrigin$log10ratioCPM>=1),]) # Most likely form Spontaneum
dim(countsOrigin[which(countsOrigin$log10ratioCPM<=-1),]) # Most likely form Officinarum

dim(countsOrigin)[1]
#Genes with mapped reads
dim(countsOrigin)[1]*100/origNumberGenes

#Proportion Genes with mapped reads assigned to common
dim(countsOrigin[which(countsOrigin$log10ratioCPM>-1 & countsOrigin$log10ratioCPM<1),])[1]*100/dim(countsOrigin)[1]
#Proportion Genes with mapped reads assigned to spontaneum
dim(countsOrigin[which(countsOrigin$log10ratioCPM>=1),])[1]*100/dim(countsOrigin)[1] 
#Proportion Genes with mapped reads assigned to offcinarum
dim(countsOrigin[which(countsOrigin$log10ratioCPM<=-1),])[1]*100/dim(countsOrigin)[1] 

countsOrigin$Origin<-NA
countsOrigin[which(countsOrigin$log10ratioCPM>-1 & countsOrigin$log10ratioCPM<1),'Origin']<-'Common'
countsOrigin[which(countsOrigin$log10ratioCPM>=1),'Origin']<-'S._spontaneum'
countsOrigin[which(countsOrigin$log10ratioCPM<=-1),'Origin']<-'S._officinarum'
head(countsOrigin)
ggplot(as.data.frame(countsOrigin),aes(x=CPM_SOFF, y=CPM_SSPO)) +
  theme(text=element_text(size=20))+
  theme_bw()+
  geom_jitter(aes(colour=Origin),alpha=0.1)+
  xlab('Log10 CPM S. officinarum')+
  ylab('Log10 CPM S. spontaneum')+
  scale_x_log10()+
  scale_y_log10()
write.table(countsOrigin, sep = "\t", file = "speciesOfOriginSP803280-Combinado.csv")

tx2gene<-read.delim("txp.group.tsv",sep=',',header=T)
head(tx2gene)
length(unique(tx2gene$GeneID))
length(unique(tx2gene$TranscriptID))
