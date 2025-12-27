import pandas as pd
import numpy as np
import argparse

# Scopo predirre le classi di sequenza -- Creazione di una matrice X binaria per ogni cromosoma

# (N finestre genomiche) × (N profili di cromatina)
# in cui:
# Ogni riga corrisponde a una finestra genomica fissa (4 kb con step 100 bp)
# Ogni colonna corrisponde a un profilo di cromatina (e.g., brain_f_42_mo|h3k4me1|None)
# Ogni valore X[i, j] = 1 se il profilo j è presente (cioè ha un overlap) nella finestra i (check tra finestre fisse con le regioni indicate nel BED file)
# Riassimendo, al profilo di indice j viene associato 1 se la window i fissa (4kb con step 100 bp) ha un overlap all'interno del BED file per una regione (end-start) corrispondete al profilo di cromatina

# Passaggi del codice:
# Caricamento del file cromatine_profiles_dlabrax.txt
# Caricamento del BED file sui nostri dati sequenzati attraverso ATAC e ChiP-seq (dlabrax_sorted_atac_chip-seq_chrs1-24.bed)
# Costruizione delle finestre genomiche (4kb tile ogni 100bp) per ogni bin specifico, come fatto dal paper di SEI ("We selected 30 million genomic positions that uniformly tile the genome with 100bp step size
# 635 and then computed Sei predictions for 4kb sequences centered at each position.")
# Creazione della matrice X di presenza/assenza dei profili per ciascuna finestra
# Salvataggio X.npy

def load_profile_names(profile_names_path):
    with open(profile_names_path) as f:
        profiles = [line.strip() for line in f]
    return profiles, {p: i for i, p in enumerate(profiles)}

def load_bed(bed_path):
    return pd.read_csv(bed_path, sep="\t", header=None, names=["chrom", "start", "end", "profile"])

def make_tiles(chrom, chrom_length, tile_size=4000, stride=100):
    tiles = []
    for start in range(0, chrom_length - tile_size + 1, stride):
        end = start + tile_size
        tiles.append((chrom, start, end))
    return tiles
# per il cromosoma una lista ove ogni nodo e' (chrom, start, end)
# La funzione make_tiles non prende le coordinate dal file BED, perché serve a generare finestre fisse e regolari lungo il genoma per tutta la lunghezza
# (esattamente come nel paper di SEI).

def build_matrix(bed_df, tiles, profile_to_index, n_profiles):
    X = np.zeros((len(tiles), n_profiles), dtype=np.uint8) # init X con la lunghezza della lista di title e il numero di profili

    for i, (chrom, t_start, t_end) in enumerate(tiles): # qui faccio uso di end e start region del BED file e lo confronto con i corrispettivi delle finestre fisse
        overlaps = bed_df[
            (bed_df["chrom"] == chrom) &
            (bed_df["start"] < t_end) &
            (bed_df["end"] > t_start) # collezione degli overlap tra le windows fisse e quelle del BED file: contiene chr, start, end, profile
        ]
        for prof in overlaps["profile"]: # scorro i profili che hanno un overlap
            if prof in profile_to_index: # se il profilo e' uno di quelli che ho definito nel file txt (e indicizzato)
                j = profile_to_index[prof]
                X[i, j] = 1 # i indice dato dalla window fissa, j indice del profilo di cromatina
    return X

def main(bed_path, profile_names_path, chrom, chrom_length, output_path):
    print("Data loaded...")
    profile_names, profile_to_index = load_profile_names(profile_names_path)
    bed_df = load_bed(bed_path)

    print("Building genomic tides...")
    tiles = make_tiles(chrom, chrom_length) # lunghezze delle finestre fisse 4000bp per 100bp (da paper SEA)


    print("Building X matrix...")
    X = build_matrix(bed_df, tiles, profile_to_index, len(profile_names))

    print(f"Saved in: {output_path}")
    np.save(output_path, X)
    print("Done!")

if __name__ == "__main__":
    # informazioni da dare in input al termiale per la compilazione: BED, profili di cromatina,
    parser = argparse.ArgumentParser()
    parser.add_argument("--bed", required=True, help="Path BED file")
    parser.add_argument("--profiles", required=True, help="Path chromatine_profiles.txt file")
    parser.add_argument("--chrom", required=True, help="Bin name (eg. CAJNNU010000001.1)")
    parser.add_argument("--length", type=int, required=True, help="bin length in bp")
    parser.add_argument("--output", default="X.npy", help="output file name")

    args = parser.parse_args()

    main(args.bed, args.profiles, args.chrom, args.length, args.output)


# FROM TERNIMAL
# General example
# python createX_fromBEDfile.py \
#    --bed bins.bed \
#    --profiles profile_names.txt \
#    --chrom CAJNNU010000001.1 \
#   --length 1000000 \
#   --output X.npy

# My example
# python createX_fromBEDfile.py \
#    --bed dlabrax_sorted_atac_chip-seq_chrs1-24.bed \
#    --profiles cromatine_profiles_dlabrax.txt \
#    --chrom CAJNNU010000001.1 \
#   --length 1000000 \
#   --output Xc1.npy