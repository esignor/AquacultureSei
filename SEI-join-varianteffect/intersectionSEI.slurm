#!/bin/bash

#SBATCH --job-name intersectionSEI
#SBATCH --output intersectionSEIOut.txt
#SBATCH --error intersectionSEIError.txt
#SBATCH --mail-user eleonora.signo@unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 35-00:00:00
# use many CPU if not using CUDA
#SBATCH --cpus-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 200G

cd sei-framework


# Eseguo il primo comando
srun apptainer exec --nv sei_gpuDEIClusters_new.sif python SEI-join-varianteffect/intersection_Ensembl_SEI.py




