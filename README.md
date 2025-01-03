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

The ancestral allele file for GRCh38 can be downloade from https://ftp.ensembl.org/pub/release-112/fasta/ancestral_alleles/ 
For GRCh37 please visit: https://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/
Try opening the link with Google Chrome(it didn't work with edge in my case). 
Download folders Homo_Sapiens_ancestor_grch37.tz

Basic Format required by Panderas
Position  Allele
Example of Format(tab-delimited format):
```
16050075  G
16050103  A
16055683  T
```

Thus the ancestral allele file should be modified into the format as specified above. You can try by your own or use the script below (in linux):

```bash
#converting the ensembl ancestral allele file to the format supported by polaris
for i in {1..22}; do
    input_file="homo_sapiens_ancestor_${i}.fa"
    output_file="hs_ancestral_chr${i}_hg19_formatted.txt"
    grep -v "^>" "$input_file" | tr -d '\n' | fold -w1 | nl > "$output_file"
done
```

### Recombination Map Files for Polarization: One per chromosome. 
The PLINK genetic map files (i.e., reference maps from https://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/) 
For GRCh38: https://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/plink.GRCh38.map.zip
For GRCh37: https://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/plink.GRCh37.map.zip

Basic Format for genetic map is different for Beagle and Panderas:
The one that we download from the above specified website is in format accepted by beagle, while the format required for Panderas is:

GeneticDistance PhysicalPosition
Example of Format(white space delimited columns).
:
```
16050000 0.123456   
16060000 0.125678  
16070000 0.128901   
```
### Recombination Map Files for BeaglePolarization: One per chromosome. 
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

