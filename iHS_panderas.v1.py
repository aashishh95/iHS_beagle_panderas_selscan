import subprocess
import os

def run_command(command):
    """Helper function to run shell commands"""
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def split_chromosomes(plink_file):
    """Split chromosomes, create VCF files, and gzip them"""
    for i in range(1, 23):
        output_prefix = f"{plink_file}_chr{i}"
        run_command(f"plink2 --bfile {plink_file} --chr {i} --recode vcf --out {output_prefix}")
        run_command(f"gzip -f {output_prefix}.vcf")
    print("Chromosome splitting completed.")

def phase_genotypes(plink_file, beagle_jar, recomb_map_dir):
    """Phase genotypes using Beagle"""
    for i in range(1, 23):
        map_file = f"{recomb_map_dir}/plink.chr{i}.GRCh37.map"
        input_vcf = f"{plink_file}_chr{i}.vcf.gz"
        output_prefix = f"{plink_file}_chr{i}_phased"
        run_command(f"java -jar {beagle_jar} gt={input_vcf} map={map_file} out={output_prefix} chrom={i}")
        run_command(f"bcftools index -t {output_prefix}.vcf.gz")
    print("Genotype phasing completed.")

def split_population(sample_file, plink_file):
    """Split VCF files by population based on sample.txt file"""
    sample_file_with_ext = f"{sample_file}.txt"
    for i in range(1, 23):
        input_vcf = f"{plink_file}_chr{i}_phased.vcf.gz"
        output_vcf = f"{sample_file}_chr{i}_phased.vcf.gz"
        run_command(f"bcftools view --samples-file {sample_file_with_ext} {input_vcf} -Oz -o {output_vcf}")
        # Tabix index the VCF after splitting by population
        run_command(f"tabix -p vcf {output_vcf}")
    print("Population splitting and indexing completed.")

def polarize_variants(panderas_path, ancestral_dir, genetic_map_dir, sample_file):
    """Polarize variants using Panderas"""
    for i in range(1, 23):
        input_vcf = f"{sample_file}_chr{i}_phased.vcf.gz"
        ancestral_file = f"{ancestral_dir}/hs_ancestral_chr{i}_hg19_formatted_output.txt"
        genetic_map = f"{genetic_map_dir}/mod_genetic_map_GRCh37_chr{i}.txt"
        output_prefix = f"{sample_file}_polarized_chr{i}"
        run_command(f"{panderas_path} -v {input_vcf} -c {i} --ancestor {ancestral_file} --genetic-map {genetic_map} -o {output_prefix}")
    print("Polarization completed.")

def run_selscan(sample_file):
    """Run selscan for iHS analysis"""
    for i in range(1, 23):
        input_hap = f"{sample_file}_polarized_chr{i}.hap"
        input_map = f"{sample_file}_polarized_chr{i}.map"
        output_prefix = f"{sample_file}_chr{i}_iHS"
        run_command(f"selscan --ihs --hap {input_hap} --map {input_map} --maf 0.01 --max-extend 1000000 --max-gap 500000 --gap-scale 50000 --cutoff 0.05 --alt --out {output_prefix}")
        run_command(f"norm --ihs --bins 100 --files {output_prefix}.ihs.alt.out")
        run_command(f"awk 'BEGIN{{OFS=\",\"; FS=\"\\t\"}} {{for(i=1; i<=NF; i++) {{printf \"\\\"%s\\\"\", $i; if(i<NF) printf \",\"}}; printf \"\\n\"}}' {output_prefix}.ihs.alt.out.100bins.norm > {output_prefix}.csv")
    print("iHS analysis completed.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="iHS Workflow for Selection Scans")
    parser.add_argument("--plink_file", required=True, help="Base PLINK file prefix")
    parser.add_argument("--sample_file", required=True, help="Sample file prefix (no extension)")
    parser.add_argument("--ancestral_dir", required=True, help="Directory containing ancestral allele files")
    parser.add_argument("--panderas_path", required=True, help="Path to Panderas executable")
    parser.add_argument("--beagle_jar", required=True, help="Path to Beagle JAR file")
    parser.add_argument("--recomb_map_dir", required=True, help="Directory containing recombination map files")
    parser.add_argument("--genetic_map_dir", required=True, help="Directory containing genetic map files")  # New argument
    args = parser.parse_args()

    # Create a directory for intermediate and output files
    os.makedirs(args.sample_file, exist_ok=True)

    # Workflow steps
    split_chromosomes(args.plink_file)
    phase_genotypes(args.plink_file, args.beagle_jar, args.recomb_map_dir)
    split_population(args.sample_file, args.plink_file)
    polarize_variants(args.panderas_path, args.ancestral_dir, args.genetic_map_dir, args.sample_file)
    run_selscan(args.sample_file)

