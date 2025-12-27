import numpy as np

# e' un array che contiene gli indici dei profili di cromatina che sono histone

histone_marks = ["h3k4me1", "h3k4me3","h3k27ac", "h3k27me3"]

histone_inds = []

with open("cromatine_profiles_dlabrax_carpio_maximus_mykiss_salmosalar.txt") as f:
    for i, line in enumerate(f):
        for mark in histone_marks:
            if mark in line.lower():
                histone_inds.append(i)
                break

histone_inds = np.array(histone_inds)
np.save("histone_inds_dlabrax_carpio_maximus_mykiss_salmosalar.npy", histone_inds)

print(f"Created histone_inds.npy with {len(histone_inds)} histione marks.")
