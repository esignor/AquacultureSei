from selene_sdk.samplers import RandomPositionsSampler
from selene_sdk.sequences import Genome
from selene_sdk.utils import load_features_list
import numpy as np

# Caricamento oggetti come da YAML
sampler = RandomPositionsSampler(
    target_path="/home/eleonora/Scrivania/sei-framework/train/data/sorted_sei_data.bed.gz",
    reference_sequence=Genome(
        input_path="/home/eleonora/Scrivania/sei-framework/resources/hg38_UCSC.fa",
        blacklist_regions="hg38"
    ),
    features=load_features_list(
        "/home/eleonora/Scrivania/sei-framework/train/data/sei_chromatin_profiles.txt"
    ),
    test_holdout=["chr8", "chr9"],
    validation_holdout=["chr10"],
    sequence_length=4096,
    center_bin_to_predict=[2048, 2049],
    mode="validate"
)

# Preleviamo un batch di esempio
sample = sampler.sample(batch_size=64)

# Stampa struttura del sample
print(f"Tipo di sample: {type(sample)}")
print(f"Numero di elementi nel sample: {len(sample)}")

# Assegnazione dinamica in base al contenuto
if len(sample) == 2:
    inputs, targets = sample
elif len(sample) == 4:
    inputs, targets, sample_ids, coordinates = sample
else:
    raise ValueError("Formato inatteso del batch restituito.")

# Diagnostica distribuzione dei target
print("Shape targets:", targets.shape)
print("Min:", targets.min())
print("Max:", targets.max())
print("Media:", targets.mean())
print("N. target > 0:", (targets > 0).sum())
print("N. target == 0:", (targets == 0).sum())
