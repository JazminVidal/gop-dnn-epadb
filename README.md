# Kaldi GOP-DNN on Epa-DB

This repository has the tools to run a Kaldi-based GOP-DNN algorithm on Epa-DB, a database of non-native English speech by Spanish speakers from Argentina. It uses a TDNN-F chain model which is downloaded from the Kaldi website.

If you use this code or database, please cite the following paper:

*J. Vidal, L. Ferrer, L. Brambilla, "EpaDB: a database for the development of pronunciation assessment systems", [isca-speech](https://www.isca-speech.org/archive/Interspeech_2019/abstracts/1839.html)*

```
@article{vidal2019epadb,
  title={EpaDB: a database for development of pronunciation assessment systems},
  author={Vidal, Jazmin and Ferrer, Luciana and Brambilla, Leonardo},
  journal={Proc. Interspeech 2019},
  pages={589--593},
  year={2019}
}
```


## Table of Contents
* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [How to install](#how-to-install)
* [How to run](#how-to-run)
* [References](#references)


## Introduction

This toolkit is meant to facilitate experimentation with Epa-DB by allowing users to run a state-of-the-art baseline system on it.
Epa-DB, is a database of non-native English speech by argentinian speakers of Spanish. It is intended for research on mispronunciation detection
and development of pronunciation assessment systems.
The database includes recordings from 50 non-native speakers of English, 25 male and 25 female, whose first language (L1) is Spanish from Argentina (mainly of the Rio de la Plata dialect).
Each speaker recorded 64 short Englsh phrases phonetically balanced and specifically designed to globally contain all the sounds difficult to pronounce for the target population.
All recordings were annotated at phone level by two expert raters.
For the sake of simplicity we followed, when possible, the organization given by the L2-ARCTIC corpus.

For more information on the database, please refer to the [documentation](https://drive.google.com/file/d/1lYQwehQ28vvayv1GABASIlMhiSTuHnU9/view?usp=sharing) or [publication](https://www.isca-speech.org/archive/Interspeech_2019/abstracts/1839.html)

If you are only looking for the EpaDB corpus, you can download it from this [link](https://drive.google.com/file/d/1Fp1LOhTMGPNO_qA5V97XNSBxbjct9P34/view?usp=sharing).

## Prerequisites

1. [Kaldi](http://kaldi-asr.org/) installed.

2. [TextGrid managing library] installed using [pip](https://pypi.org/project/praat-textgrids/).

3. [The EpaDB database](https://drive.google.com/file/d/1Fp1LOhTMGPNO_qA5V97XNSBxbjct9P34/view?usp=sharing) downloaded. Alternative [link](https://www.dropbox.com/s/13ylpy846hq3d7p/epadb.zip?dl=0)

## How to install

To install this repository, do the following steps:

1. Clone this repository:
```
git clone https://github.com/JazminVidal/gop-dnn-epadb.git
```

2. Check the requirements.txt file:

```
pip install -r requirements.txt
```

3. Set the following lines in the file gop-dnn-epadb/path.sh:
```
export KALDI_ROOT=path/to/where/your/kaldi-trunk/is
export EPADB_ROOT=path/to/where/epadb/is
export GOPEPA_REPO_ROOT=/path/to/where/gop-dnn-epadb-repo/is
```

## How to run

1. Run data_preparation.sh to create the necessary directories and files. This script creates soft links to wsj folders in Kaldi, downloads and extracts the acoustic and language models from kaldi web, computes mfcc's, extracts i-vectors and creates temporary folders from EpaDB files.

```
./data_preparation.sh
```

2. Run run.sh to compute alignments a goodness of pronunciation scores. Results will be stored under exp folder. You should expect to find alignments, gop and prob files, among others.

```
./run.sh
```

3. Run the evaluation script to compute labels for EpaDB and match them to the gop results. Labels are computed by comparing the manual annotations in annotations_1 to all the possible correct transcriptions in trans_complete file. Alignments from different systems not always coincide. To sort this problem out the script also matches EpaDB alignments with those computed along the gop script. Results are stored under results folder. You should expect to obtain a pickle file with all the information necessary to compute metrics and a folder with EpaDB labels.

```
./run_eval.sh
```
4. Run the plotter script to obtain metrcs and plots.




## References

* Hu, Wenping, Yao Qian, and Frank K. Soong. "An improved DNN-based approach to mispronunciation detection and diagnosis of L2 learners' speech." SLaTE. 2015. [link](https://www.slate2015.org/files/submissions/Hu15-AID.pdf)

* Povey, Daniel, et al. "Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks." Interspeech. 2018. [link](https://www.danielpovey.com/files/2018_interspeech_tdnnf.pdf)
