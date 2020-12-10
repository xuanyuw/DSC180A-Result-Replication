args <- commandArgs(trailingOnly = TRUE)
gene_matrix <- args[1]
run_table <- args[2]
out_gene_matrix <- args[3]
out_run_table <- args[4]
pasCts <- gene_matrix
pasAnno <- run_table
cts <- as.matrix(read.csv(pasCts))
coldata <- read.csv(pasAnno)
cts <- cts[1:100, 1:101]
coldata <- subset(coldata, coldata$Run %in% colnames(cts))
write.csv(cts, out_gene_matrix)
write.csv(coldata, out_run_table, row.names=FALSE)