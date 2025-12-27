import pandas as pd
import gzip
import random

# Lista dei profili (puoi estendere fino a 50+)
profiles = ['A549|ELF1|EtOH_0.02pct','MCF7|CTCF|DMSO_0.1pct','K562|GATA3|TNFa_10ngml','HepG2|FOXA1|EtOH_0.05pct','HeLa|MYC|DMSO_0.01pct','HCT116|SP1|IL6_20ngml','U2OS|TP53|EtOH_0.1pct','SKBR3|ESR1|DMSO_0.5pct','A549|NFKB1|TNFa_5ngml','MCF10A|AP1|EtOH_0.02pct','K562|CEBPB|IL1b_10ngml','HepG2|STAT3|EtOH_0.03pct','HeLa|YY1|DMSO_0.2pct','HCT116|BCL6|TNFa_15ngml','U2OS|ZEB1|EtOH_0.04pct','SKBR3|AR|DHT_10nM','A549|FOXP1|EtOH_0.01pct','MCF7|RUNX1|DMSO_0.05pct','K562|E2F1|TNFa_25ngml','HepG2|HNF4A|EtOH_0.1pct','HeLa|NFYA|DMSO_0.3pct','HCT116|ETS1|IL6_50ngml','U2OS|SMAD3|EtOH_0.07pct','SKBR3|STAT1|IFNg_20ngml','A549|FOXA2|EtOH_0.02pct','MCF7|MAZ|DMSO_0.4pct','K562|MAX|TNFa_1ngml','HepG2|PBX1|EtOH_0.06pct','HeLa|USF1|DMSO_0.15pct','HCT116|IRF1|IL1b_15ngml','U2OS|BACH1|EtOH_0.08pct','SKBR3|SRF|Serum_10pct','A549|ATF3|EtOH_0.03pct','MCF7|JUN|DMSO_0.2pct','K562|TCF7L2|TNFa_30ngml','HepG2|CREB1|EtOH_0.09pct','HeLa|SMARCA4|DMSO_0.25pct','HCT116|FOXO3|IL6_10ngml','U2OS|IKZF1|EtOH_0.02pct','SKBR3|EGR1|DMSO_0.6pct','A549|ZFX|EtOH_0.04pct','MCF7|RELA|DMSO_0.35pct','K562|CHD1|TNFa_20ngml','HepG2|KLF4|EtOH_0.01pct','HeLa|GABPA|DMSO_0.45pct','HCT116|SOX9|IL1b_5ngml','U2OS|STAT5A|EtOH_0.05pct','SKBR3|ETS2|IFNg_50ngml','A549|ZEB2|EtOH_0.02pct','MCF7|FOSL1|DMSO_0.3pct']

# Leggi il file BED compresso
bed = pd.read_csv("/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/train/data/50-sorted_sei_data.bed.gz", sep="\t", compression="gzip", header=None)


# Assicurati che ci siano almeno 3 colonne
assert bed.shape[1] >= 3, "Il file BED deve avere almeno 3 colonne"

# Assegna profili (scegli uno dei due metodi):

# Metodo 1: Ciclico
bed[3] = [profiles[i % len(profiles)] for i in range(len(bed))]

# Metodo 2: Casuale (decommenta per usarlo)
# bed[3] = [random.choice(profiles) for _ in range(len(bed))]

# Salva il nuovo file come .bed.gz
bed.to_csv("/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/train/data/simulated.bed.gz", sep="\t", header=False, index=False, compression="gzip")

