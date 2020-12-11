args <- commandArgs(trailingOnly = TRUE)

img_dir <- args[1]
gene_matrix <- args[2]
run_table <- args[3]

if(args[4] == "TRUE") {
  test_mode <<- TRUE
} else {
  test_mode <<- FALSE
}

# install packages
#if (!requireNamespace("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")

#BiocManager::install("DESeq2")
#BiocManager::install("pasilla")
#BiocManager::install("apeglm")

# import packages
#library("pasilla")
library("DESeq2")


# get data
pasCts <- gene_matrix
pasAnno <- run_table
cts <- as.matrix(read.csv(pasCts, row.names = "target_id"))
coldata <- read.csv(pasAnno, row.names=1)
# subsetting data
coldata <- subset(coldata, rownames(coldata) %in% colnames(cts))
coldata <- coldata[c("age_at_death", "post.mortem_interval", "Brain_pH", "clinical_diagnosis", "source_name")]
coldata <- coldata[complete.cases(coldata), ]
# sort to be in the same order
cts <- cts[, rownames(coldata)]
cts <-round(cts, 0)
#pre-filter
if(test_mode == FALSE){
  keep <- rowSums(cts) >= 3000
  cts <- cts[keep, ]
}
#pseudo-count to avoid DESeq error
cts[cts == 0] <- 1


# plot pca
dds_pca <- DESeqDataSetFromMatrix(countData = cts,
                                  colData = coldata,
                                  design = ~ age_at_death + post.mortem_interval + 
                                    Brain_pH + clinical_diagnosis)
if(test_mode==TRUE) {
  vsd_pca <- vst(dds_pca, blind=FALSE, nsub = 50)
} else{
  vsd_pca <- vst(dds_pca, blind=FALSE)
}
png(filename = paste(img_dir, "pca.png", sep = ''), height = 300, width = 500)
plotPCA(vsd_pca, intgroup="source_name")
dev.off()

#subsetting counts based on groups
ancg_sz_info <- coldata[coldata$source_name %in% c("AnCg_Schizophrenia", "AnCg_Control"), ]
dlpfc_sz_info <-coldata[coldata$source_name %in% c("DLPFC_Schizophrenia", "DLPFC_Control"), ]
nacc_sz_info <-coldata[coldata$source_name %in% c("nAcc_Schizophrenia", "nAcc_Control"), ]
ancg_bpd_info <-coldata[coldata$source_name %in% c("AnCg_Bipolar Disorder", "AnCg_Control"), ]
dlpfc_bpd_info <-coldata[coldata$source_name %in% c("DLPFC_Bipolar Disorder", "DLPFC_Control"), ]
nacc_bpd_info <-coldata[coldata$source_name %in% c("nAcc_Bipolar Disorder", "nAcc_Control"), ]
ancg_mdd_info <-coldata[coldata$source_name %in% c("AnCg_Major Depression", "AnCg_Control"), ]
dlpfc_mdd_info <-coldata[coldata$source_name %in% c("DLPFC_Major Depression", "DLPFC_Control"), ]
nacc_mdd_info <-coldata[coldata$source_name %in% c("nAcc_Major Depression", "nAcc_Control"), ]

ancg_sz <- cts[,colnames(cts)%in%rownames(ancg_sz_info)]
dlpfc_sz <- cts[,colnames(cts)%in%rownames(dlpfc_sz_info)]
nacc_sz <- cts[,colnames(cts)%in%rownames(nacc_sz_info)]
ancg_bpd <- cts[,colnames(cts)%in%rownames(ancg_bpd_info)]
dlpfc_bpd <- cts[,colnames(cts)%in%rownames(dlpfc_bpd_info)]
nacc_bpd <- cts[,colnames(cts)%in%rownames(nacc_bpd_info)]
ancg_mdd <- cts[,colnames(cts)%in%rownames(ancg_mdd_info)]
dlpfc_mdd <- cts[,colnames(cts)%in%rownames(dlpfc_mdd_info)]
nacc_mdd <- cts[,colnames(cts)%in%rownames(nacc_mdd_info)]

# generate DESeq2 results
get_DESeq_res <- function(countData, colData){
  dds <- DESeqDataSetFromMatrix(countData = countData,
                                colData = colData,
                                design = ~ age_at_death + post.mortem_interval + 
                                  Brain_pH + clinical_diagnosis)
  #LRT
  dds <- DESeq(dds, test="LRT", reduced=~1)
  res <- results(dds)
  return(res)
}
ancg_sz_res = get_DESeq_res(ancg_sz, ancg_sz_info)
dlpfc_sz_res = get_DESeq_res(dlpfc_sz, dlpfc_sz_info)
nacc_sz_res = get_DESeq_res(nacc_sz, nacc_sz_info)

ancg_bpd_res = get_DESeq_res(ancg_bpd, ancg_bpd_info)
dlpfc_bpd_res = get_DESeq_res(dlpfc_bpd, dlpfc_bpd_info)
nacc_bpd_res = get_DESeq_res(nacc_bpd, nacc_bpd_info)

ancg_mdd_res = get_DESeq_res(ancg_mdd, ancg_mdd_info)
dlpfc_mdd_res = get_DESeq_res(dlpfc_mdd, dlpfc_mdd_info)
nacc_mdd_res = get_DESeq_res(nacc_mdd, nacc_mdd_info)

# generate histograms
if (!require("ggplot2")) install.packages("ggplot2")
library(ggplot2)
plot_hist <- function(values, color){
  plot <- ggplot(as.data.frame(values), aes(x=values)) + 
    geom_histogram(color="black", fill=color)+ ylab("Frequency") +
    ylim(NA, 4000) + theme_bw() +
    theme(axis.line = element_line(colour = "black"),
          axis.title.x=element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank(),
          panel.background = element_blank()) 
  return(plot)
}
require(gridExtra)

display_hist <-function(df, color){
  # exclude any sample with base mean less than 10
  copy <- df[df$baseMean>10, ]
  hist_plot <- plot_hist(copy[copy$padj<1 & !is.na(copy$padj), "padj"], color)
  return(hist_plot)
}

png(filename = paste(img_dir, "hist_plots.png", sep = ''), height = 900, width = 900)
ancg_sz_plot <- display_hist(ancg_sz_res, "red")
dlpfc_sz_plot <- display_hist(dlpfc_sz_res, "blue")
nacc_sz_plot <- display_hist(nacc_sz_res, "green")

ancg_bpd_plot <- display_hist(ancg_bpd_res, "red")
dlpfc_bpd_plot <- display_hist(dlpfc_bpd_res, "blue")
nacc_bpd_plot <- display_hist(nacc_bpd_res, "green")

ancg_mdd_plot <- display_hist(ancg_mdd_res, "red")
dlpfc_mdd_plot <- display_hist(dlpfc_mdd_res, "blue")
nacc_mdd_plot <- display_hist(nacc_mdd_res, "green")

grid.arrange(arrangeGrob(ancg_sz_plot, top = "AnCg", left = "SZ", bottom = "P-value"), 
             arrangeGrob(dlpfc_sz_plot, top = "DLPFC", bottom = "P-value"), 
             arrangeGrob(nacc_sz_plot, top = "nAcc", bottom = "P-value"), 
             arrangeGrob(ancg_bpd_plot, left = "BPD"), 
             dlpfc_bpd_plot, 
             nacc_bpd_plot, 
             arrangeGrob(ancg_mdd_plot, left = "MDD"), 
             dlpfc_mdd_plot, 
             nacc_mdd_plot, ncol=3, nrow=3)
dev.off()

# generate correlation plots
if (!require("corrplot")) install.packages("corrplot")
library(corrplot)
Ancg <- data.frame("SZ"=ancg_sz_res$log2FoldChange, 
                   "BPD"=ancg_bpd_res$log2FoldChange,
                   "MDD"=ancg_mdd_res$log2FoldChange)
Dlpfc <- data.frame("SZ"=dlpfc_sz_res$log2FoldChange, 
                    "BPD"=dlpfc_bpd_res$log2FoldChange,
                    "MDD"=dlpfc_mdd_res$log2FoldChange)
nAcc <- data.frame("SZ"=nacc_sz_res$log2FoldChange, 
                   "BPD"=nacc_bpd_res$log2FoldChange,
                   "MDD"=nacc_mdd_res$log2FoldChange)

png(filename = paste(img_dir, "corr_plots.png", sep = ''), height = 600, width = 200)
par(mfrow=c(3, 1))
ancg_plot <- corrplot.mixed(cor(Ancg, use = "complete.obs", method = "spearman"), 
                            title = "AnCg", mar=c(0,0,1,0))
dlpfc_plot <- corrplot.mixed(cor(Dlpfc, use = "complete.obs", method = "spearman"),
                             title = "DLPFC", mar=c(0,0,1,0))
nacc_plot <- corrplot.mixed(cor(nAcc, use = "complete.obs", method = "spearman"), 
                            title = "nAcc", mar=c(0,0,1,0))
par(mfrow=c(1, 1))
dev.off()

# generate Venn diagrams
if (!require("VennDiagram")) install.packages("VennDiagram")
library(VennDiagram)
if(!require("RColorBrewer")) install.packages("RColorBrewer")
library(RColorBrewer)
myCol <- brewer.pal(3, "Pastel2")

# Chart
plot_venn <- function(sz_sig, bpd_sig, mdd_sig){
  venn_plot <- venn.diagram(
    x = list(sz_sig, bpd_sig, mdd_sig),
    category.names = c("SZ" , "BPD " , "MDD"),
    filename = NULL, 
    
    # Circles
    lwd = 0,
    lty = 'blank',
    fill = myCol,
    
    # Numbers
    cex = .6,
    fontface = "bold",
    fontfamily = "sans",
    
    # Set names
    cat.cex = 0.6,
    cat.fontface = "bold",
    cat.fontfamily = "sans",
  )
}
# use adjusted pval
ancg_sz_sig <- rownames(ancg_sz_res[which(ancg_sz_res$padj <0.05), ])
ancg_bpd_sig <- rownames(ancg_bpd_res[which(ancg_bpd_res$padj <0.05), ])
ancg_mdd_sig <- rownames(ancg_mdd_res[which(ancg_mdd_res$padj <0.05), ])

dlpfc_sz_sig <- rownames(dlpfc_sz_res[which(dlpfc_sz_res$padj <0.05), ])
dlpfc_bpd_sig <- rownames(dlpfc_bpd_res[which(dlpfc_bpd_res$padj <0.05), ])
dlpfc_mdd_sig <- rownames(dlpfc_mdd_res[which(dlpfc_mdd_res$padj <0.05), ])

nacc_sz_sig <- rownames(nacc_sz_res[which(nacc_sz_res$padj <0.05), ])
nacc_bpd_sig <- rownames(nacc_bpd_res[which(nacc_bpd_res$padj <0.05), ])
nacc_mdd_sig <- rownames(nacc_mdd_res[which(nacc_mdd_res$padj <0.05), ])


png(filename = paste(img_dir, "venn_diagrams.png", sep = ''), height = 300, width = 900)
library(gridExtra)
grid.arrange(arrangeGrob(gTree(children=plot_venn(ancg_sz_sig, ancg_bpd_sig, ancg_mdd_sig)),
                           top = "AnCg"), 
               arrangeGrob(gTree(children=plot_venn(dlpfc_sz_sig, dlpfc_bpd_sig, dlpfc_mdd_sig)),
                           top = "DLPFC"),
               arrangeGrob(gTree(children=plot_venn(nacc_sz_sig, nacc_bpd_sig, nacc_mdd_sig)),
                           top = "nAcc"),
               ncol=3)
dev.off()

# Perform heirarchial clustering
if (!require("dendextend")) install.packages("dendextend")
library(dendextend)
library(RColorBrewer)

plot_hc <- function(cnts, info, sig, disorder){
  if(test_mode==TRUE){
    hc_cnts <- cnts
  } else {
    hc_cnts <- cnts[rownames(cnts)%in%sig, ]
  }
  
  dds <- DESeqDataSetFromMatrix(countData = hc_cnts,
                                colData = info,
                                design = ~ age_at_death + post.mortem_interval 
                                + Brain_pH + clinical_diagnosis)
  dds <- DESeq(dds, test="LRT", reduced=~1, fitType="mean")
  if(test_mode==TRUE){
    vsd <- vst(dds, blind=FALSE, nsub = 3)
  }else{
    vsd <- vst(dds, blind=FALSE)
  }
  
  dists <- dist(t(assay(vsd)), method = "euclidean")
  hc <- hclust(dists, method = "ward.D2")
  dend <- as.dendrogram(hc)
  o.dend <- order.dendrogram(dend)
  vsd$clinical_diagnosis <- as.character(vsd$clinical_diagnosis)
  vsd$clinical_diagnosis[vsd$clinical_diagnosis!="Control"] <- disorder
  vsd$clinical_diagnosis <- as.factor(vsd$clinical_diagnosis)
  labels(dend) <- vsd$clinical_diagnosis[o.dend]
  labels_colors(dend) <- as.integer(vsd$clinical_diagnosis[o.dend])
  return(dend)
}

png(filename = paste(img_dir, "hierarchical_clusters.png", sep = ''), height = 900, width = 900)
par(mfrow = c(3, 3))
hc_ancg_sz <- plot(plot_hc(ancg_sz, ancg_sz_info, ancg_sz_sig, "SZ"), main = "AnCg x SZ")
hc_dlpfc_sz <- plot(plot_hc(dlpfc_sz, dlpfc_sz_info, dlpfc_sz_sig, "SZ"), main = "DLPFC x SZ")
hc_nacc_sz <- plot(plot_hc(nacc_sz, nacc_sz_info, nacc_sz_sig, "SZ"), main = "nAcc x SZ")

hc_ancg_bpd <- plot(plot_hc(ancg_bpd, ancg_bpd_info, ancg_bpd_sig, "BPD"), main = "AnCg x BPD")
hc_dlpfc_bpd <- plot(plot_hc(dlpfc_bpd, dlpfc_bpd_info, dlpfc_bpd_sig, "BPD"), main = "DLPFC x BPD")
hc_nacc_bpd <- plot(plot_hc(nacc_bpd, nacc_bpd_info, nacc_bpd_sig, "BPD"), main = "nAcc x BPD")

hc_ancg_mdd <- plot(plot_hc(ancg_mdd, ancg_mdd_info, ancg_mdd_sig, "MDD"), main = "AnCg x MDD")
hc_dlpfc_mdd <- plot(plot_hc(dlpfc_mdd, dlpfc_mdd_info, dlpfc_mdd_sig, "MDD"), main = "DLPFC x MDD")
hc_nacc_mdd <- plot(plot_hc(nacc_mdd, nacc_mdd_info, nacc_mdd_sig, "MDD"), main = "nAcc x MDD")
par(mfrow = c(1, 1))
dev.off()



