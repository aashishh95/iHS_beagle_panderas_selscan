# Overview
This workflow automates the computation of integrated Haplotype Scores (iHS) to detect signals of selection in genomic data. The script performs tasks like chromosome splitting, phasing, population filtering, variant polarization, and finally, iHS calculation.

# Required Tools for this workflow
```
PLINK 2: For chromosome splitting and data preprocessing.
Beagle: For genotype phasing.
BCFtools: For VCF filtering and indexing.
Panderas: For polarizing variants using ancestral allele data. Please visit https://github.com/alisi1989/Polaris for more details on Polaris/Panderas
Selscan: For iHS calculations.
```

# Required Input file

### PLINK Binary Files: 
```
.bed
.bim
.fam
```
### Sample File: A .txt file containing the list of individuals. 
Format (FID_IID):

```
1_GSA-01
9_GSA-02
10_GSA-18
17_GSA-03
18_GSA-19
25_GSA-04
26_GSA-20
33_GSA-07
```
### Ancestral Allele Files: Pre-formatted for each chromosome.

Given the space limitations on GitHub, the Homo_sapiens_hg38_reference file from Ensembl for each chromosome (https://ftp.ensembl.org/pub/release-112/fasta/ancestral_alleles/) is stored separately in DropBox (https://www.dropbox.com/scl/fo/0du8z7xoeqs5qqr73qk2s/ADuGddGTZXwUIeZkmQZ-geM?rlkey=tn11q5yt2yohyuu5q3ube2x88&st=qzjtapey&dl=0) and are available for downloaded. If users wish to incorporate a different ancestral allele reference file, they will need to make sure the file is in a tab-delimited format (please see below).

For hg37 please visit: https://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/
Try opening the link with google Chrome. Download folders Homo_Sapiens_ancestor_grch37.tz

Basic Format
Position  Allele
Example of Format:
```
16050075  G
16050103  A
16055683  T
```
Ancestral allele file modification can be done as(in command line):

#converting the ensembl ancestral allele file to the format supported by polaris

```bash
for i in {1..22}; do
    input_file="homo_sapiens_ancestor_${i}.fa"
    output_file="hs_ancestral_chr${i}_hg19_formatted.txt"
    grep -v "^>" "$input_file" | tr -d '\n' | fold -w1 | nl > "$output_file"
done
```

### Recombination Map Files for Polarization: One per chromosome. 
The PLINK genetic map files (i.e., reference maps from https://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/) are provided in DropBox (https://www.dropbox.com/scl/fo/b3a9z16sqjvksprqudlpg/ACv4xl3Nk9HHZP0m4Em0CVI?rlkey=7dqtaioskwnk2u8mgcx1osui9&st=ultsv8k1&dl=0). Genetic map files should contain the genetic position and physical position in white space delimited columns.

For GRCh37: https://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/plink.GRCh37.map.zip

Basic Format:
GeneticDistance PhysicalPosition
Example of Format:
```
16050000 0.123456   
16060000 0.125678  
16070000 0.128901   
```
### Recombination Map Files for Polarization: One per chromosome. 
See Format: (tab deliminated columns)
```
22	.	0.010291	16052618
22	.	0.018472	16053624
22	.	0.018756	16053659
22	.	0.019561	16053758
22	.	0.027325	16054713
22	.	0.029307	16054960
```
# Script execution

Please check bash_iHS_panderas.sh. I usually create a conda environment after installing selscan within the created conda environment, activate the conda environment and run the bash script as job.

```bash
chmod +x bash_iHS_panderas.sh

sbatch bash_iHS_panderas.sh
```


# Output files
```
Chromosome-specific VCF files (.vcf.gz) and their indexes (.tbi).
Phased VCF files for each chromosome.
Population-filtered VCF files.
Polarized haplotype files.
iHS results in .csv format.
```

