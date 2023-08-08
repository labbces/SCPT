rm(list=ls())
library(ggplot2)
setwd("/data/diriano/checkInflation/")
data<-read.delim("panTranscriptomeDistributionSizeOrthogroupsTable_AllInflation.tsv",header=F,col.names = c("OG","AvgSize",'Inflation'),dec='.')
data$Inflation<-as.factor(data$Inflation)
head(data)
ggplot(data, aes(x=AvgSize, fill=Inflation))+ 
  theme_bw()+
  geom_histogram(bins=200, position='dodge') + 
  scale_x_log10()+
  scale_y_log10()

library(cogeqc)
#Loading annotation files
pfam_B1<-read.delim("B1_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_B2<-read.delim("B2_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_CC011940<-read.delim("CC011940_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_Co06022<-read.delim("Co06022_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_Co8021<-read.delim("Co8021_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_CoV92102<-read.delim("CoV92102_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_CP742005<-read.delim("CP74-2005_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_F1Bulk1<-read.delim("F1-Bulk-1_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_F1Bulk2<-read.delim("F1-Bulk-2_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_FN951702<-read.delim("FN95-1702_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_GN18<-read.delim("GN18_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_GT96167<-read.delim("GT96-167_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_GUC10<-read.delim("GUC10_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_GUC2<-read.delim("GUC2_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_GXU34140<-read.delim("GXU-34140_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_GXU34176<-read.delim("GXU-34176_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQ082850<-read.delim("KQ08-2850_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0723863<-read.delim("KQB07-23863_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0723990<-read.delim("KQB07-23990_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0724619<-read.delim("KQB07-24619_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0724739<-read.delim("KQB07-24739_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0832953<-read.delim("KQB08-32953_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0920432<-read.delim("KQB09-20432_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0920620<-read.delim("KQB09-20620_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_KQB0923137<-read.delim("KQB09-23137_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_LCP85384<-read.delim("LCP85-384_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_MS6847<-read.delim("MS6847_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_MT11610<-read.delim("MT11-610_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_Q200<-read.delim("Q200_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_Q241<-read.delim("Q241_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QA021009<-read.delim("QA02-1009_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QA961749<-read.delim("QA96-1749_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QBYN0426041<-read.delim("QBYN04-26041_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QC02402<-read.delim("QC02-402_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QN051460<-read.delim("QN05-1460_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QN051509<-read.delim("QN05-1509_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QN051743<-read.delim("QN05-1743_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QN05803<-read.delim("QN05-803_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_QS992014<-read.delim("QS99-2014_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_R570<-read.delim("R570_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_RB72454<-read.delim("RB72454_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_RB855156<-read.delim("RB855156_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_ROC20<-read.delim("ROC20_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_ROC22<-read.delim("ROC22_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_ROC26<-read.delim("ROC26_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_SP803280<-read.delim("SP80-3280_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_T1<-read.delim("T1_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_T2<-read.delim("T2_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_TUC717<-read.delim("TUC717_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)
pfam_US851008<-read.delim("US851008_PEP.fix.nr100.ALL.pfam.tblout.tbl", col.names = c("Gene","Annotation"),header=FALSE)




annotation=list(
  B1 = pfam_B1,
  'B2' = pfam_B2,
  'CC011940' = pfam_CC011940,
  'Co06022' = pfam_Co06022,
  'Co8021' = pfam_Co8021,
  'CoV92102' = pfam_CoV92102,
  'CP74.2005' = pfam_CP742005,
  'F1.Bulk.1' = pfam_F1Bulk1,
  'F1.Bulk.2' = pfam_F1Bulk2,
  'FN95.1702' = pfam_FN951702,
  'GN18' = pfam_GN18,
  'GT96.167' = pfam_GT96167,
  'GUC10' = pfam_GUC10,
  'GUC2' = pfam_GUC2,
  'GXU.34140' = pfam_GXU34140,
  'GXU.34176' = pfam_GXU34176,
  'KQ08.2850' = pfam_KQ082850,
  'KQB07.23863' = pfam_KQB0723863,
  'KQB07.23990' = pfam_KQB0723990,
  'KQB07.24619' = pfam_KQB0724619,
  'KQB07.24739' = pfam_KQB0724739,
  'KQB08.32953' = pfam_KQB0832953,
  'KQB09.20432' = pfam_KQB0920432,
  'KQB09.20620' = pfam_KQB0920620,
  'KQB09.23137' = pfam_KQB0923137,
  'LCP85.384' = pfam_LCP85384,
  'MS6847' = pfam_MS6847,
  'MT11.610' = pfam_MT11610,
  'Q200' = pfam_Q200,
  'Q241' = pfam_Q241,
  'QA02.1009' = pfam_QA021009,
  'QA96.1749' = pfam_QA961749,
  'QBYN04.26041' = pfam_QBYN0426041,
  'QC02.402' = pfam_QC02402,
  'QN05.1460' = pfam_QN051460,
  'QN05.1509' = pfam_QN051509,
  'QN05.1743' = pfam_QN051743,
  'QN05.803' = pfam_QN05803,
  'QS99.2014' = pfam_QS992014,
  'R570' = pfam_R570,
  'RB72454' = pfam_RB72454,
  'RB855156' = pfam_RB855156,
  'ROC20' = pfam_ROC20,
  'ROC22' = pfam_ROC22,
  'ROC26' = pfam_ROC26,
  'SP80.3280' = pfam_SP803280,
  'T1' = pfam_T1,
  'T2' = pfam_T2,
  'TUC717' = pfam_TUC717,
  'US851008' = pfam_US851008
  )
length(annotation)

orthogroups_I1.2 <- read_orthogroups("Orthogroups_I1.2.tsv")
orthogroups_I1.6 <- read_orthogroups("Orthogroups_I1.6.tsv")
orthogroups_I2.0 <- read_orthogroups("Orthogroups_I2.0.tsv")
orthogroups_I2.4 <- read_orthogroups("Orthogroups_I2.4.tsv")
orthogroups_I2.8 <- read_orthogroups("Orthogroups_I2.8.tsv")
orthogroups_I3.2 <- read_orthogroups("Orthogroups_I3.2.tsv")
orthogroups_I3.6 <- read_orthogroups("Orthogroups_I3.6.tsv")
orthogroups_I4.0 <- read_orthogroups("Orthogroups_I4.0.tsv")
orthogroups_I4.4 <- read_orthogroups("Orthogroups_I4.4.tsv")
orthogroups_I4.8 <- read_orthogroups("Orthogroups_I4.8.tsv")
orthogroups_I5.2 <- read_orthogroups("Orthogroups_I5.2.tsv")
orthogroups_I5.6 <- read_orthogroups("Orthogroups_I5.6.tsv")
orthogroups_I6.0 <- read_orthogroups("Orthogroups_I6.0.tsv")
head(orthogroups_I1.2)

#og_assessment_I1.2 <- assess_orthogroups(orthogroups_I1.2, annotation)
data_res<-as.data.frame(matrix(data=NA,ncol=2,nrow=13))
colnames(data_res)<-c('Inflation','MeanScore')

count=1
for (i in seq(from=1.2,to=6.0,by=0.4)){
  i2=format(round(i,2),nsmall=1)
  print(i2)
  p<-eval(as.symbol(paste("orthogroups_I",i2,sep='')))
  og_assessment <- assess_orthogroups(p, annotation)
  data_res[count,1]<-i2
  data_res[count,2]<-mean(og_assessment$Mean_score)
  count=count+1
}

data_res
ggplot(data_res, aes(x=Inflation,y=MeanScore))+
  theme_bw()+
  geom_point()
#mean(og_assessment_I1.2$Mean_score)
#sps<-unique(orthogroups_I1.2$Species)
