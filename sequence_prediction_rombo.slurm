#!/bin/bash

#SBATCH --job-name 2sequence_prediction
#SBATCH --output 2sequenceprediction-rombo_BESTMODEL-Out.txt
#SBATCH --error 2sequenceprediction-rombo_BESTMODEL-Err.txt
#SBATCH --mail-user eleonora.signor@unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 1-00:00:00
# use many CPU if not using CUDA
#SBATCH --cpus-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 200G
# uncomment to use GPU
##SBATCH --gres=gpu:rtx

cd sei-framework

input_filepath="${1:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/Seque_rombo.fa}"
hg_version="${2:-maximus}"
out_dir="${3:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/sequenceprediction_maximus}"
cuda="${4:---cuda}"
input_filepath_hdf5="${5:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/sequenceprediction_maximus/chromatin-profiles-hdf5/Seque_rombo_predictions.h5}"


# Eseguo il primo comando
# srun apptainer exec --nv sei_gpuDEIClusters_new.sif bash 1_sequence_prediction.sh $input_filepath $hg_version $out_dir $cuda

# Eseguo il secondo comando
srun apptainer exec --nv sei_gpuDEIClusters_new.sif bash 2_raw_sc_score.sh $input_filepath_hdf5 $out_dir

