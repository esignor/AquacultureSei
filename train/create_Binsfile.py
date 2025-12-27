import csv
import gzip

# File di input/output
bed_file = '/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/train/data/sorted_sei_data.bed.gz'
profiles_file = '/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/train/data/10-sei_chromatin_profiles.txt'
output_file = '/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/train/data/10-sorted_sei_data.bed'

# 1. Carica i profili da includere
with open(profiles_file, 'r') as pf:
    included_profiles = set(line.strip() for line in pf if line.strip())

# 2. Filtra i bins nel file BED
filtered_bins = []
with gzip.open(bed_file, 'rt') as bf:  # usa gzip e 'rt' per leggere in testo
    reader = csv.reader(bf, delimiter='\t')
    for row in reader:
        if len(row) < 4:
            continue  # Salta righe mal formate
        profile = row[3].encode('utf-8').decode('utf-8').strip()
        if profile in included_profiles:
            filtered_bins.append(row)

# 3. Ordina per cromosoma (colonna 0) e posizione (colonna 1)
filtered_bins.sort(key=lambda x: (x[0], int(x[1])))

# 4. Scrive il file filtrato e ordinato
with open(output_file, 'w', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerows(filtered_bins)

print(f"File salvato: {output_file} con {len(filtered_bins)} righe.")

# se avessi problemi con gli spazi
# per rimuovere '/r' direttamente dal file e.g,. zcat 50-sorted_sei_data.bed.gz | tr -d '\r' > 50-sorted_sei_data_cleaned.bed