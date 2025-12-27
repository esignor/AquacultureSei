import os
import subprocess

bed_file = "dlabrax_sorted_atac_chip-seq_chrs1-24.bed"
profiles_file = "cromatine_profiles_dlabrax.txt"
length = "1000000" # parametro tecnico di slicing, per efficienza computazionale cosi se il cromosoma e' troppo lungo carico solo `length` basi per volta

chr_start = 10; chr_end = 25
for i in range(chr_start, chr_end):
    chrom = f"CAJNNU01000000{i}.1"
    output_file = f"Xc{i}.npy"

    cmd = [
        "python", "createX_fromBEDfile.py",
        "--bed", bed_file,
        "--profiles", profiles_file,
        "--chrom", chrom,
        "--length", length,
        "--output", output_file
    ]

    print(f"Run to {chrom} → {output_file}")
    subprocess.run(cmd)
