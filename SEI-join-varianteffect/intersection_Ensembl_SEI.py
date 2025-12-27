import pandas as pd
from pandas.api.types import CategoricalDtype

# === Funzione per calcolare la colonna con massimo effetto assoluto ===
def get_max_effect_column(row):
    values = row[['C0','C1','C2','C3','C4','C5','C6']].fillna(0).astype(float)
    return values.abs().idxmax()

# === STEP 1: Load df2 (variant_effects_subclasses_margins.csv) ===
file = 'run3_dlabraxSNPdlabrax-variant_effects_subclasses_margins.csv'
cols = ['chr_pos','margin','ref','alt','C0','C1','C2','C3','C4','C5','C6']

# Leggi CSV correttamente saltando l'intestazione già presente
df2 = pd.read_csv(
    'SEI-join-varianteffect/dlabrax/' + file,
    sep=',',
    names=cols,
    header=0,   
    engine='python'
)

# Converte margin e C0-C6 in float
df2['margin'] = pd.to_numeric(df2['margin'], errors='coerce')
for col in ['C0','C1','C2','C3','C4','C5','C6']:
    df2[col] = pd.to_numeric(df2[col], errors='coerce').astype('float32')

# === STEP 2: Load df1 (data_Ensembl.csv) ===
df1 = pd.read_csv('SEI-join-varianteffect/dlabrax/data_Ensembl.csv', sep='\t', dtype={
    'chr_pos': str,
    'funct': 'category',
    'n_tissue': 'uint8'
})
df1.columns = df1.columns.str.strip()

# === STEP 3: Left merge ===
df_merge = pd.merge(df2, df1, on='chr_pos', how='left')

# === STEP 4: Reorder columns ===
df_merge = df_merge[['chr_pos', 'margin', 'funct', 'ref', 'alt', 'n_tissue',
                     'C0','C1','C2','C3','C4','C5','C6']]

# === STEP 5: Save raw intersection ===
df_merge.to_csv('SEI-join-varianteffect/dlabrax/intersection_run3_dlabraxSNPdlabrax-variant_effects_subclasses_margins.csv',
                index=False, na_rep='N/A')

# === STEP 6: Remove duplicates keeping highest margin ===
df_no_na = df_merge.copy()
df_no_na['margin'] = pd.to_numeric(df_no_na['margin'], errors='coerce')

df_nodup = df_no_na.sort_values('margin', ascending=False).drop_duplicates(subset='chr_pos', keep='first')

# Gestione colonne categoriche
if isinstance(df_nodup['funct'].dtype, CategoricalDtype):
    df_nodup['funct'] = df_nodup['funct'].cat.add_categories('N/A')

# === STEP 6.5: Calculate max_effect safely ===
# Assicurati che C0-C6 siano float
for col in ['C0','C1','C2','C3','C4','C5','C6']:
    df_nodup[col] = pd.to_numeric(df_nodup[col], errors='coerce')

df_nodup['max_effect'] = df_nodup.apply(get_max_effect_column, axis=1)

# === STEP 7: Fill NaN e save final file ===
df_nodup = df_nodup.fillna('N/A')
df_nodup = df_nodup.sort_values(by='margin', ascending=False)

df_nodup.to_csv('SEI-join-varianteffect/dlabrax/intersection_run3_dlabraxSNPdlabrax-variant_effects_subclasses_margins-nodump.csv',
                index=False, na_rep='N/A')
