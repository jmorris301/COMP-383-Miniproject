import os
from Bio import SeqIO
import datetime
import csv

directory = os.popen('pwd').read().rstrip()
path = (directory + '/OptionA_Jack_Morris/')
os.system('mkdir ' + path)
os.chdir(path)

# Get .sra files
os.system('wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra')

# fastq-dump
os.system('fastq-dump -I --split-files SRR8185310.sra')



#Running Spades
os.system('spades -k 55,77,99,127 -t 2 --only-assembler -s SRR8185310_1.fastq -o ' + path)

# Spades command
command = 'spades -k 55,77,99,127 -t 2 --only-assembler -s SRR8185310_1.fastq -o ' + path
#print(command)

# Writing command to OptionA.log
# Beginning OptionA.log file
log = open(path + "/OptionA.log","w+")
for i in range(1):
	log.write("Spades Command: " + command + "\n" + "\n")



# Python script to keep contigs with lengths > 1000

Over_1000_Sequences=[]

with open(path + "contigs.fasta", "rU") as handle:
	for record in SeqIO.parse(handle, "fasta"):
		if len(record.seq) > 1000:
          # Add this record to our list
              		Over_1000_Sequences.append(record)

long_assembly = ("There are %i contigs > 1000 in the assembly." % len(Over_1000_Sequences))
#print(long_assembly)

# Write to fasta
SeqIO.write(Over_1000_Sequences, "long_sequences.fasta", "fasta")

# Write to OptionA.log
log = open(path + "/OptionA.log","a+")
for i in range(1):
	log.write(long_assembly + "\n" + "\n")



# Python script for total assembly reads for contigs > 1000
length = 0
temp = 0
for record in SeqIO.parse('long_sequences.fasta', 'fasta'):
        temp = len(record)
        length += temp
final_length = str(length)
total_length = ('There are ' + str(length) + ' bp in the assembly.')
#print(total_length)

# Write to OptionA.log
log = open(path + "/OptionA.log","a+")
for i in range(1):
	log.write(total_length + "\n" + "\n")



# Run Prokka

os.system('prokka --force --outdir ' + path + 'Prokka_Output/ --genus Escherichia --locustag ECOL long_sequences.fasta')

# Write to OptionA.log
prokka_command = "prokka --outdir " + path + "Prokka_Output/ --genus Escherichia --locustag ECOL long_sequences.fasta"
log = open(path + "/OptionA.log","a+")
for i in range(1):
	log.write("\n" + prokka_command + "\n" + "\n")



# Writing Results of Prokka to OptionA.log

now = datetime.datetime.now()
temp = (str(now))

  #Month day year
month = (now.month)
day = ("%d" % now.day)
year = ("%d" % now.year)

if month >= 10:
	current_date = (month+day+year)
#	print(current_date)
else:
	month = ("0" + str(month))
	current_date = (month+day+year)
#       print(current_date)


file_name = "PROKKA_" + current_date + ".txt"

with open(path + 'Prokka_Output/' + file_name) as temp:
	with open(path + "/OptionA.log", "a+") as only:
		for x in temp:
	    		only.write(x)


# Writing discrepancies of Prokka annotation to the RefSeq

file_data = open(path + "Prokka_Output/" + file_name)
CDS= 4140
TRNA = 89

for x in file_data:
	if x.startswith('CDS'):
		cds_line = x[5:]
            	#print(a)
	if x.startswith('tRNA'):
		trna_line = x[5:]

cds_line = int(cds_line)
cds_count = CDS - cds_line

trna_line = int(trna_line)
trna_count = TRNA - trna_line

if cds_count > 0:
	x = "less"
elif cds_count <0:
	x = "additional"
	cds_count = abs(cds_count)
if trna_count > 0:
	n = "less"
elif trna_count<0:
	n = "additional"
	trna_count = abs(trna_count)

final = ("Prokka found " + str(cds_count) + " " + x + " CDS and " + str(trna_count) + " " + n + " tRNA than the RefSeq.")
#print(final)

# Write to log file
append = open(path + "/OptionA.log", "a+")
for n in range(1):
	append.write(final)



# Getting RefSeq file
os.system('wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR141/SRR1411276/SRR1411276.sra')

# Using fastq-dump
os.system('fastq-dump -I SRR1411276.sra')

# Retrieving .fna file
os.system('wget ftp://ftp.ncbi.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna')

# Using Bowtie2:
os.system('bowtie2-build NC_000913.fna EcoliK12')

# Using Tophat:
os.system('tophat --no-novel-juncs -o ' + path + ' EcoliK12 SRR14112976.fastq')

# Using Cufflinks:
os.system('cufflinks -p 2 accepted_hits.bam')



# Note: Option1.fpkm file created, but contents of Cufflinks output never written to it
# Input and output
file = open('transcripts.gtf')
fpkm_input = open('Option1.fpkm','w')

format = csv.writer(fpkm_input, delimiter=',')

# Calling writerow to write out parameters for Option1.fpkm
format.writerow(['seqname','start','end','strand','FPKM'])
