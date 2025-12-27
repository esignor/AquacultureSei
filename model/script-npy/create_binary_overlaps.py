import numpy as np
import glob


# Script per generare projvec_targets.npy: Matrice binaria (N windows x P profiles)
# Unisco tutte le matrice binarie (che contengono l'informazione sul overlap dei profili sulle windows), concatenata verticalmente per ogni cromosoma
# E' LA MATRICE ORIGINARIA DI INPUT PER LE SUCCESSIVE TRASFORMAZIONI

## singola specie
# Trova e ordina i file Xc*.npy (assicurati che siano tutti nella stessa cartella)
#X_files = sorted(glob.glob("XBin_overlaps/carpio/Xc*.npy")) 

# Carica e concatena verticalmente
#X_all = np.concatenate([np.load(f) for f in X_files], axis=0)

# Salva il file finale
#np.save("projvec_targets.npy", X_all)
#print(f"Created projvec_targets.npy with shape {X_all.shape}")


## multispecie
X_files = sorted(glob.glob("XBin_overlaps/carpio/Xc*.npy"))
X_files += sorted(glob.glob("XBin_overlaps/maximus/Xc*.npy"))

arrays = [np.load(f) for f in X_files]
max_cols = max(arr.shape[1] for arr in arrays)

# Pad con zeri a destra
padded_arrays = [np.pad(arr, ((0,0),(0, max_cols - arr.shape[1])), mode='constant') 
                 for arr in arrays]

X_all = np.concatenate(padded_arrays, axis=0)
np.save("binary_overlaps_carpio_maximus.npy", X_all)
print(f"Created binary_overlaps_carpio_maximus.npy with shape {X_all.shape}")