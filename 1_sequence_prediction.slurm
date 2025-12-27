#!/bin/bash

#SBATCH --job-name 1_sequence_prediction
#SBATCH --output 1_sequence_predictionOut.txt
#SBATCH --error 1_sequence_predictionErr.txt
#SBATCH --mail-user eleonora.signor@studenti.unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 35-00:00:00
# use many CPU if not using CUDA
#SBATCH --cpus-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 200G
# uncomment to use GPU
#SBATCH --gres=gpu:rtx

cd sei-framework

input_filepath="${1:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/BED/dlabrax_sorted_atac_chip-seq_chrs1-24.bed}"
hg_version="${2:-dlabrax}"
out_dir="${3:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/test-sequence_prediction}"
cuda="${4:---cuda}"


# Eseguo il primo comando
srun apptainer exec --nv sei_gpuDEIClusters_new.sif bash 1_sequence_prediction.sh $input_filepath $hg_version $out_dir $cuda

