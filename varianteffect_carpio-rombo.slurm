#!/bin/bash

#SBATCH --job-name 2varianteffect
#SBATCH --output 2varianteffect-carpiorombo_BESTMODEL-Out.txt
#SBATCH --error 2varianteffect-carpiorombo_BESTMODEL-Err.txt
#SBATCH --mail-user eleonora.signor@unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 5-00:00:00
# use many CPU if not using CUDA
#SBATCH --cpus-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 500G
# uncomment to use GPU
##SBATCH --gres=gpu:rtx

cd sei-framework
## in utils.py cambia il numero di cluster in base a quante sono quelle definite in _.names
vcf_filepath="${1:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/varianteffects_allIDs.vcf}"
hg_version="${2:-dlabrax}" ## reference genome della specie delle varianti (dlabrax)
outdir="${3:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/varianteffects-exp3_outputs_carpio-rombo}"
cuda="${4:---cuda}"
ref_fp="${5:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/varianteffects-exp3_outputs_carpio-rombo/chromatin-profiles-hdf5/varianteffects_allIDs.ref_predictions.h5}"
alt_fp="${6:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/varianteffects-exp3_outputs_carpio-rombo/chromatin-profiles-hdf5/varianteffects_allIDs.alt_predictions.h5}"
out_dir="${7:-/nfsd/bcb/bcbg/EleonoraSignor/sei-framework/varianteffects-exp3_outputs_carpio-rombo}"
no_tsv="${8:-}"


# Eseguo il primo comando
# srun apptainer exec --nv sei_gpuDEIClusters_new.sif bash 1_variant_effect_prediction.sh $vcf_filepath $hg_version $outdir $cuda

# Eseguo il secondo comando
srun apptainer exec --nv sei_gpuDEIClusters_new.sif bash 2_varianteffect_sc_score.sh $ref_fp $alt_fp $out_dir
