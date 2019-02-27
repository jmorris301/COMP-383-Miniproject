## EcoliK12 Miniproject Option A

This is the repository running my python script which will automate assembly and annotation for the resequencing of EcoliK12 sequences. The purpose of resequencing is due to the ever evolving nature of the Ecoli K12 strain. This has required researchers to resequence it to track its evolution over time relative to the original K12 strain. 

### Prior Installation ###
* Python 3
* SPAdes v3.11.1
* Prokka
* tophat v2.1.1
* bowtie v1.2.2
* cufflinks v2.2.1
* SRA-toolkit
* wget

### Running the pipeline ###
`$ git clone https://github.com/jmorris301/COMP-383-Miniproject.git`

This will download two file types. One is the Python script EcoliK12.py and this README.md.


### Output ###
After running the script, all files and subdirectories in the pipeline will be automatically written to a directory called `OptionA_Jack_Morris`.
Certain command outputs and pipeline information will be written to a file called `OptionA.log`.
Another file will be written called `Option1.fpkm` which contains Cufflinks output in a .csv format.
