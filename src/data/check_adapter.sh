echo "$1"
cd src/data
TMP_DIR='tmp'
mkdir -p $TMP_DIR
/opt/FastQC/fastqc "$1" -o $TMP_DIR
cd $TMP_DIR
for filename in *.zip
do
unzip $filename
done
SUBSTRING=$(echo $1| cut -d'.' -f 1)
FOLDER="${SUBSTRING}_fastqc"
cd $(echo $FOLDER| cut -d'/' -f 4)
grep -w -F "Adapter" summary.txt >> ../adapter_info.txt
