import pandas as pd
from collections import defaultdict

# === INPUT ===
vcf_file = "seabasses/varianteffects_allIDs.vcf"
csv_file = "seabasses/SNP_array_seabass.csv"
out_file = "seabasses/varianteffects_allIDs_ESACTALT.vcf"

# === STEP 1: Carica genotipi dal CSV ===
print("Lettura genotipi...")
df = pd.read_csv(csv_file)

# Mappa SNP -> basi osservate (da genotipi)
observed_alleles = defaultdict(set)

for snp_col in df.columns[1:]:  # salta la colonna ID
    for genotype in df[snp_col].dropna():
        for base in genotype:  # "AG" -> "A","G"
            observed_alleles[snp_col].add(base)

# === STEP 2: Leggi VCF originale ===
print("Lettura VCF originale...")
vcf_data = pd.read_csv(
    vcf_file,
    sep="\t",
    header=None,
    names=["chrom", "pos", "id", "ref", "alt"]
)

# === STEP 3: Costruisci nuovo VCF ===
print("Generazione nuovo VCF...")
vcf_out_rows = []

for (chrom, pos), group in vcf_data.groupby(["chrom", "pos"]):
    snp_id = f"{chrom}:{pos}"
    ref = group["ref"].iloc[0]
    observed = observed_alleles.get(snp_id, set())

    # Alleli alternativi = osservati (escludendo il ref)
    #alt_bases = sorted(a for a in observed if a != ref)

#    if alt_bases:
#        alt_string = ",".join(alt_bases)
#        vcf_out_rows.append([chrom, pos, ".", ref, alt_string])


    # Alleli alternativi = osservati, escludendo il ref e eventuali '0'
    alt_bases = sorted(a for a in observed if a != ref and a != '0')

    for alt in alt_bases:
        vcf_out_rows.append([chrom, pos, ".", ref, alt])

# === STEP 4: Scrivi output ===
out_df = pd.DataFrame(vcf_out_rows, columns=["chrom", "pos", "id", "ref", "alt"])
out_df.to_csv(out_file, sep="\t", header=False, index=False)

print(f"File generato: {out_file}")
