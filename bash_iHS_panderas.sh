#!/bin/bash

# Define the resource requirements here using #SBATCH
#SBATCH -c 10  # Requesting 10 CPUs
#SBATCH -t 24:00:00  # Max wallTime for the job
#SBATCH --mem=128G  # Requesting 128G memory
#SBATCH -o job.%J.out  # Output file
#SBATCH -e job.%J.err  # Error file

# Check if conda is initialized, if not, initialize it
if ! command -v conda &> /dev/null
then
    echo "Conda not found. Initializing conda..."
    conda init
fi

# Activate the Conda environment only if it's not already activated
if [[ "$CONDA_DEFAULT_ENV" != "selscan" ]]; then
    echo "Activating conda environment: selscan"
    conda activate selscan
else
    echo "Conda environment 'selscan' is already activated."
fi

# Check if required modules are loaded; load them if not
module_list=$(module list 2>&1)

if [[ ! "$module_list" =~ "gencore/2" ]]; then
    echo "Loading module: gencore/2"
    module load all gencore/2
else
    echo "Module 'gencore/2' is already loaded."
fi

if [[ ! "$module_list" =~ "beagle" ]]; then
    echo "Loading module: beagle"
    module load beagle
else
    echo "Module 'beagle' is already loaded."
fi

if [[ ! "$module_list" =~ "bcftools" ]]; then
    echo "Loading module: bcftools"
    module load bcftools
else
    echo "Module 'bcftools' is already loaded."
fi

python /scratch/ag10818/github_popgen/iHS_panderas/iHS_panderas.v1.py \
    --plink_file dataset \
    --sample_file population \
    --ancestral_dir /scratch/ag10818/github_popgen/iHS_panderas/ancestral_allele_ensembl_hg19 \
    --panderas_path /scratch/ag10818/github_popgen/iHS_panderas/Panderas \
    --beagle_jar /scratch/ag10818/softwares/beagle.28Jun21.220.jar \
    --recomb_map_dir /scratch/ag10818/github_popgen/iHS_panderas/recomb_map_hg19 \
    --genetic_map_dir /scratch/ag10818/github_popgen/iHS_panderas/recomb_map_hg19

#concatenate all the csv files
for i in {1..22}; do
    cat "population_chr${i}_iHS.csv" >> brokpa_samples_allChr.csv
done
