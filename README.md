# Sei-Aquaculture Extension

This repository contains an extension of the [SEI framework](https://github.com/FunctionLab/sei-framework), adapted for genomic data analysis in aquaculture species. The SEI framework is licensed for academic and research use only; see *LICENSE.txt* for details.

## License

The original code (SEI framework) is distributed under the following license:

*Copyright (c) 2021 The Trustees of Princeton University, The Simons Foundation, Inc. 
and The University of Texas Southwestern Medical Center. All rights reserved.
Redistribution and use in source and binary forms, with or without modification, 
are permitted for academic and research use only.* See [LICENSE.txt](LICENSE.txt) for full details.


Please note that all modifications and extensions in this repository follow the same academic/research use restrictions.

## Highlights of Extension

* Adapted SEI framework for **aquaculture species**: European sea bass, carp, rainbow trout, turbot, and Atlantic salmon.

* Developed **multi-species model training** with genome concatenation, unique chromosome identifiers, and merged regulatory peaks.

* Integrated **large-scale SNP datasets** from AQUA-FAANG, enabling prediction of regulatory effects for sea bass and other species.

* Customized **chromatin profile-based deep learning models** for single- and multi-species predictions.

* Extended **variant effect prediction pipeline**, allowing assessment of non-coding SNP impacts on chromatin regulation.

## Overview

This extension supports both **single-species** and **multi-species** models, allowing analysis of chromatin regulatory patterns and **SNP functional predictions across aquaculture species**. Multi-species integration enables discovery of shared regulatory signals while preserving species-specific characteristics.

## Datasets

Datasets consist of **reference genomes** and **chromatin profiles** obtained from ATAC-seq and ChIP-seq experiments, mostly sourced from [Ensembl](https://www.ensembl.org/index.html) and the **AQUA-FAANG project**. Regulatory peaks mapped to very short contigs were excluded to ensure data consistency.

## Model Architecture

The **SEI architecture** includes:

- Convolutional networks with dual linear and nonlinear paths

- Residual dilated convolutional layers

- Spatial basis function transformation and output layers

Linear blocks facilitate learning linear dependencies, while nonlinear blocks include ReLU activations, convolution, and batch normalization. Residual connections and dilated convolutions expand receptive fields without losing spatial information. A B-spline transformation reduces spatial dimensionality while preserving discrimination of genomic patterns.

## Training and Evaluation

**Framework:** Selene, integrated with SEI

**Environment:** Singularity container for NVIDIA RTX 3090 GPUs

**Optimizer:** SGD, learning rate 0.001, momentum 0.9, weight decay 1e-7

**Loss:** Binary cross-entropy

**Data split:** ~70% training, 20% validation, 10% test; bins from each chromosome assigned together

**Hyperparameters:** sequence length 4096 bp, central bin [2048,2049], batch size 64, 100,000 training steps

**Metrics:** AUROC and AUPRC


## Multi-Species Integration


## Variant Effect Prediction

The model predicts non-coding variant effects using:

$$E_c = \tilde{P}_c^{\text{alt}} - \tilde{P}_c^{\text{ref}}, \qquad \text{margin} = \left|\max_c E_c\right|.$$

where $\tilde{P}_c$ is the normalized predicted probability for chromatin profile $c$. This allows assessing SNP effects on chromatin regulation.



## Computational Resources

Experiments were conducted on:

* 2 GPU nodes: 32 CPU cores, 1.5 TB RAM, 8 NVIDIA RTX 3090 GPUs each

* 3 CPU-only nodes: 48 CPU cores, 1.5 TB RAM

GPUs used for training, CPUs for variant effect prediction.


## Usage

1. Clone this repository alongside SEI Framework:

    ``git clone https://github.com/FunctionLab/sei-framework``

    ``git clone https://github.com/esignor/AquacultureSei``


2. Install dependencies from SEI and this extension.

3. Prepare genomic and regulatory datasets as described above.

4. Train single- or multi-species models using Selene.

5. Predict variant effects using the trained models.

## References

- [SEI Framework](https://github.com/FunctionLab/sei-framework)  
- [Ensembl Genome Browser](https://www.ensembl.org)  
- AQUA-FAANG project publications  

Additional relevant publications.

#### SEI Framework

Kathleen M. Chen, Aaron K. Wong, Olga G. Troyanskaya, and Jian Zhou. A sequence-based global map of regulatory activity for deciphering human genetics. Nature Genetics, 54(7):940–949, 2022

#### AQUA-FAANG project

Richard Mukiibi, Silvia Ferraresso, Raffaella Franch, Laura Peruzza, Giulia Dalla Rovere, Massimiliano Babbucci, Daniela Bertotto, Anna Toffan, Francesca Pascoli, Stefano Faggion, Cristián Peñaloza, Costas S. Tsigenopoulos, Ross D. Houston, Luca Bargelloni, and Diego Robledo. *Integrated functional genomic analysis identifies regulatory variants underlying a major QTL for disease resistance in European sea bass*. BMC Biology, 23(1):75, 2025.  

Robert Mukiibi, Serena Ferraresso, Rafaella Franch, Luca Peruzza, Giulia Dalla Rovere, Massimiliano Babbucci, Daniela Bertotto, Anna Toffan, Francesco Pascoli, Sara Faggion, Carolina Peñaloza, Costas S. Tsigenopoulos, Ross D. Houston, Luca Bargelloni, and Diego Robledo. *Integrated functional genomic analysis identifies the regulatory variants underlying a major QTL for disease resistance in European sea bass*. bioRxiv, 2024.  
