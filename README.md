# Overview
This workflow automates the computation of integrated Haplotype Scores (iHS) to detect signals of selection in genomic data. The script performs tasks like chromosome splitting, phasing, population filtering, variant polarization, and finally, iHS calculation.

# Required Tools for this workflow

PLINK 2: For chromosome splitting and data preprocessing.
Beagle: For genotype phasing.
BCFtools: For VCF filtering and indexing.
Tabix: For creating indexes on VCF files.
Panderas: For polarizing variants using ancestral allele data.
Selscan: For iHS calculations.
Norm: For normalizing iHS results.
awk: For processing and formatting output data.
Python: Script orchestration and argument handling.


# Required Input file

PLINK Binary Files: .bed, .bim, .fam.

Sample File: A .txt file containing the list of individuals.

Recombination Map Files: One per chromosome.

Ancestral Allele Files: Pre-formatted for each chromosome.

Genetic Map Files: Modified genetic map files for polarization.

#output files


Chromosome-specific VCF files (.vcf.gz) and their indexes (.tbi).
Phased VCF files for each chromosome.
Population-filtered VCF files.
Polarized haplotype files.
iHS results in .csv format.

