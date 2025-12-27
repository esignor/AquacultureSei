#!/bin/bash

#SBATCH --job-name maximus_exp22_testEval_seiframework
#SBATCH --output maximus_exp22_testEval_seiframeworkOut.txt
#SBATCH --error maximus_exp22_testEval_seiframeworkError.txt
#SBATCH --mail-user eleonora.signor@unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 35-00:00:00
# use many CPU if not using CUDA
#SBATCH --cpus-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 200G
# uncomment to use GPU
#SBATCH --gres=gpu:rtx
#SBATCH --export=ALL,MPLBACKEND=Agg,PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:64

cd sei-framework


# Eseguo il primo comando
srun apptainer exec --nv sei_gpuDEIClusters_new.sif python -m selene_sdk.cli evaluate/maximus-exp22-testEval.yml





