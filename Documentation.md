Log into mounted COMP 383 computer

cd /home/jmorris/Miniproject/

________________________________________________________________________________________________________________________________________      

1. Retrieve the Illumina reads for the resequencing of K-12 project: https://www.ncbi.nlm.nih.gov/sra/SRX5005282.
These are single-end Illumina reads. You can retrieve the sequences via:
wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra.

Retrieve data from NCBI:

  wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra

Uncompressing data with fastq-dump:

  fastq-dump -I --split-files SRR8185310.sra
  Read 4594560 spots for SRR8185310.sra
  Written 4594560 spots for SRR8185310.sra


The files we have now are:
  jmorris@comp383:~/Miniproject$ ls
  SRR8185310_1.fastq  SRR8185310.sra
#The one file output indicates it's a single-end read

________________________________________________________________________________________________________________________________________      

2. Using SPAdes, assemble the genome. Write the SPAdes command to the log file.
  jmorris@comp383:~/Miniproject$ spades -k 55,77,99,127 -t 2 --only-assembler -s SRR8185310_1.fastq -o /home/jmorris/OptionA_Jack_Morris/

  jmorris@comp383:~/Miniproject$ cd SPAdes_output/
  jmorris@comp383:~/Miniproject/SPAdes_output$ ls
  assembly_graph.fastg               before_rr.fasta  contigs.paths  input_dataset.yaml  K77  misc        scaffolds.fasta  spades.log  warnings.log
  assembly_graph_with_scaffolds.gfa  contigs.fasta    dataset.info   K55                 K99  params.txt  scaffolds.paths  tmp

________________________________________________________________________________________________________________________________________      

3. Writing Python script to keep contigs with lengths > 1000 to counting_contigs.py:
      from Bio import SeqIO

      Over_1000_Sequences=[]

      with open("/home/jmorris/Miniproject/SPAdes_output/contigs.fasta", "rU") as handle:
          for record in SeqIO.parse(handle, "fasta"):
              if len(record.seq) > 1000 :
              # Add this record to our list
                  Over_1000_Sequences.append(record)

      print("There are %i contigs > 1000 in the assembly." % len(Over_1000_Sequences))

    SeqIO.write(Over_1000_Sequences, "long_sequences.fasta", "fasta")

Running the Python Script:
  Python3 counting_contigs.py
  
________________________________________________________________________________________________________________________________________      

4. Writing Python script for total assembly reads to assembly_length.py:
    
    from Bio import SeqIO

    length = 0
    temp = 0

    for record in SeqIO.parse('/home/jmorris/Miniproject/SPAdes_output/long_sequences.fasta', 'fasta'):
        temp = len(record)
        length += temp

    final_length = str(length)
    solution = ('There are ' + str(length) + ' bp in the assembly.')
    print(solution)
    #SeqIO.write(solution, "/Users/Jack/Documents/Atom.io/COMP 383/Miniproject/Assembly_length.fasta", "fasta")

________________________________________________________________________________________________________________________________________      

5. We already have the .fasta file that we want to annotate with Prokka - it contains the long sequences > 1000
   Running Prokka with this file:
      prokka --outdir /home/jmorris/OptionA_Jack_Morris/Prokka_Output --genus Escherichia --locustag ECOL long_sequences.fasta
       
________________________________________________________________________________________________________________________________________      

6. Writing results of the .txt file to the .log file in the same format:
   Writing pyton script for it:
      #Script for gathering the current date and making sure the Prokka file is named with it
      #Prokka file is then called and written to the OptionA.log file:
      #Prokka --> .log file
         
         #Import
          import datetime
          now = datetime.datetime.now()
          temp = (str(now))

          #Month day year
          month = (now.month)
          day = ("%d" % now.day)
          year = ("%d" % now.year)

          if month >= 10:
              current_date = (month+day+year)
              print(current_date)
          else:
              month = ("0" + str(month))
              current_date = (month+day+year)
              print(current_date)


          file_name = "PROKKA_" + current_date + ".txt"

          with open("/Users/Jack/Documents/Atom.io/COMP 383/Miniproject/" + file_name) as temp:
              with open("/Users/Jack/Documents/Atom.io/COMP 383/Miniproject/OptionA.log", "w") as only:
                  for x in temp:
                      only.write(x)
  
  
  Calling file to write Prokka.txt to the OptionA.log:
      python3 Prokka_to_log.py

  Success
      
________________________________________________________________________________________________________________________________________      
      
7. Second half of Prokka_to_log.py written as:
   #This script appends the differences in the CDS and tRNA count relative to the RefSeq file to the OptionA.log
   
      file_data = open("/Users/Jack/Documents/Atom.io/COMP 383/Miniproject/" + file_name)
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
      if trna_count>0:
          n = "less"
      elif trna_count<0:
          n = "additional"
          trna_count = abs(trna_count)

      final = ("Prokka found " + str(cds_count) + " " + x + " CDS and " + str(trna_count) + " " + n + " tRNA than the RefSeq.")
      print(final)

      #Write to log file
      append = open("/Users/Jack/Documents/Atom.io/COMP 383/Miniproject/OptionA.log", "a+")
      for n in range(1):
          append.write("\n" + final)

  Success
________________________________________________________________________________________________________________________________________      

8. Need to get file from ftp:
      wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR141/SRR1411276/SRR1411276.sra
      
  Using fastq-dump to convert the file type from .sra:
      fastq-dump -I SRR1411276.sra
  
  Need to get NC_000913.fna file:
      wget 
  
  Using Bowtie2:
      bowtie2-build NC_000913.fna EcoliK12 
            
  Using Tophat:
      tophat --no-novel-juncs -o + path + EcoliK12 SRR14112976.fastq
  
  Using Cufflinks:
       cufflinks -p 2 accepted_hits.bam
  
  Success
________________________________________________________________________________________________________________________________________
  
9. 
  