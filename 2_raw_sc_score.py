"""
Description:
    This script is run after `1_sequence_prediction.py`. It computes the
    raw sequence class scores based on Sei chromatin profile predictions
    of sequences (i.e. no variants).

Usage:
    2_raw_sc_score.py <input-fp> <output-dir>
                      [--out-name=<out-name>]
    2_raw_sc_score.py -h | --help

Options:
    <input-fp>             Path to Sei sequence predictions to compute raw
                           sequence class projection scores (NO variant effect).
    <output-dir>           The directory to output the sequence class scores
                           as an .NPY file.
    --out-name=<out-name>  Specify an output filename prefix. Otherwise, output
                           filenames will be based on <input-fp>.

"""
import os

from docopt import docopt
import h5py
import numpy as np
import pandas as pd

from utils import get_filename_prefix, get_data, get_targets
from utils import sc_projection


if __name__ == "__main__":
    arguments = docopt(
        __doc__,
        version='1.0.0')
    output_dir = arguments['<output-dir>']
    os.makedirs(output_dir, exist_ok=True)

    input_pred_file = arguments['<input-fp>']
    input_preds = get_data(input_pred_file)
    print("Shape of input_preds:", input_preds.shape)
    input_dir, input_fn = os.path.split(input_pred_file)

    input_prefix = get_filename_prefix(input_fn)
    rowlabels_file = os.path.join(input_dir, '{0}_row_labels.txt'.format(
        input_prefix))
    rowlabels = pd.read_csv(rowlabels_file, sep='\t')
    if len(rowlabels) != len(input_preds):
        raise ValueError(("Rowlabels file '{0}' does not have the same number "
                          "of rows as '{1}'").format(rowlabels_file,
                                                     input_pred_file))

    output_prefix = arguments['--out-name']
    if output_prefix is None:
        output_prefix = input_fn.split('_predictions')[0]
    print("Output files will start with prefix '{0}'".format(output_prefix))

    sei_dir = "./model"
    chromatin_profiles = get_targets(os.path.join(sei_dir, "target_dlabrax2021.names"))
    seqclass_names = get_targets(os.path.join(sei_dir, "seqclass_dlabrax2021.names"))

    clustervfeat = np.load(os.path.join(sei_dir, 'projvec_targets_dlabrax2021.npy')) # (438, 103) -> (n_cluster, n_profiles)

    projscores = sc_projection(input_preds, clustervfeat)
    np.save(os.path.join(
        output_dir, "{0}.raw_sequence_class_scores.npy".format(output_prefix)),
        projscores)
    

    # --- CSV Conversion ---
    class_names = [f"Class_{i}" for i in range(projscores.shape[1])]
    df = pd.DataFrame(projscores, columns=class_names)
    df.insert(0, "Sequence", rowlabels.iloc[:,1])


    # Computation the margin maximum for each cluster
    df.insert(1, "Margin", df.iloc[:,1:].abs().max(axis=1))

    # Computation the cluster to which belongs the margin for each sequence
    df.insert(2, "Cluster_margin", df.iloc[:,2:].abs().idxmax(axis=1))

    # Numeric index of the winning cluster
    cluster_idx_numeric = df['Cluster_margin'].apply(lambda x: int(x.split('_')[1]))

    # Index profile to cluster with maximum weight in abs
    best_profile_idx_for_cluster = np.argmax(np.abs(clustervfeat), axis=1)

    # Select to each sequence the index profiles maximum, corrispontence to maximum cluster
    dominant_profile_idx = cluster_idx_numeric.apply(lambda k: best_profile_idx_for_cluster[k])

    # Convert indx of chromatine profile in name
    dominant_profile_names = [chromatin_profiles[j] for j in dominant_profile_idx]

    # Aggiungiamo al DataFrame
    df.insert(3, "Chromatin_profile", dominant_profile_names)

    
    
    # Save CSV
    csv_path = os.path.join(
        output_dir, "{0}.raw_sequence_class_scores.csv".format(output_prefix))
    df.to_csv(csv_path, index=False)
    print(f"CSV file written to {csv_path}")



