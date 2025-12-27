#!/bin/bash

#SBATCH --job-name dlabrax_exp2Train_eval_seiframework
#SBATCH --output dlabrax_exp2Train_eval_seiframeworkOut.txt
#SBATCH --error dlabrax_exp2Train_eval_seiframeworkError.txt
#SBATCH --mail-user eleonora.signor@unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 35-00:00:00
# use many CPU if not using CUDA
#SBATCH --cpus-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 200G
# uncomment to use GPU
#SBATCH --gres=gpu:rtx
#SBATCH --export=ALL,PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:64

cd sei-framework


# Eseguo il primo comando
srun apptainer exec --nv sei_gpuDEIClusters_new.sif python -m selene_sdk.cli evaluate/dlabrax-exp2-trainEval.yml





