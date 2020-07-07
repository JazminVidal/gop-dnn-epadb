# Kaldi GOP-DNN on Epa-DB

This repository has the tools to run a Kaldi-based GOP-DNN algorithm on Epa-DB, a database of non-native English speech by Spanish speakers from Argentina. It uses a TDNN-F chain model which is downloaded from the Kaldi website.

If you use this code or database, please cite the following paper:

*J. Vidal, L. Ferrer, L. Brambilla, "EpaDB: a database for the development of pronunciation assessment systems", [isca-speech](https://www.isca-speech.org/archive/Interspeech_2019/abstracts/1839.html)*

```
@article{vidal2019epadb,
  title={EpaDB: a database for development of pronunciation assessment systems},
  author={Vidal, Jazm{\i}n and Ferrer, Luciana and Brambilla, Leonardo},
  journal={Proc. Interspeech 2019},
  pages={589--593},
  year={2019}
}
```


## Table of Contents
* [Introduction](#introduction)
* [Database Overview](#Database-overview)
* [Prerequisites](#prerequisites)
* [How to install](#how-to-install)
* [How to run](#how-to-run)
* [How to evaluate](#how-to-evaluate)
* [References](#references)


## Introduction

This toolkit is meant to facilitate experimentation with Epa-DB by allowing users to run a state-of-the-art baseline system on it.
Epa-DB, is a database of non-native English speech by argentinian speakers of Spanish. It is intended for research on mispronunciation detection
and development of pronunciation assessment systems.
The database includes recordings from 50 non-native speakers of English, 25 male and 25 female, whose first language (L1) is Spanish from Argentina (mainly of the Rio de la Plata dialect).
Each speaker recorded 64 short Englsh phrases phonetically balanced and specifically designed to globally contain all the sounds difficult to pronounce for the target population.
All recordings were annotated at phone level by two expert raters.
For the sake of simplicity we followed, when possible, the organization given by the L2-ARCTIC corpus.

## Database Overview
For each speaker, the database contains:

* **Speech recordings**: 64 short English phrases (some of them may have been removed because of quality problems)
* **Word and phoneme level reference transcriptions**: Reference word and phoneme transcriptions in ARPA-bet obtained using the Montreal Forced Aligner. Boundaries were manually corrected by the raters.
* **Phoneme level manual transcriptions**: Phoneme level annotations of what the subject actually pronounced in ARPA-bet and an ARPA-bet like extension to account for those sounds not present in the English inventory.
* **Reference transcriptions**: for each utterance, the set of all the correct pronunciations in ARPA-bet. This file is useful to compute labels.

For more information on the database, please refer to the [documentation](https://drive.google.com/file/d/1lYQwehQ28vvayv1GABASIlMhiSTuHnU9/view?usp=sharing) or [publication](https://www.isca-speech.org/archive/Interspeech_2019/abstracts/1839.html)

If you are only looking for the EpaDB corpus, you can download it from this [link](https://drive.google.com/file/d/1Fp1LOhTMGPNO_qA5V97XNSBxbjct9P34/view?usp=sharing).

## Prerequisites

1. [Kaldi](http://kaldi-asr.org/) installed.

2. [TextGrid managing library](https://github.com/Legisign/Praat-textgrids) cloned or [pip](https://pypi.org/project/praat-textgrids/).

3. [The EpaDB database](https://drive.google.com/file/d/1Fp1LOhTMGPNO_qA5V97XNSBxbjct9P34/view?usp=sharing) downloaded.

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
export GOPEPA_REPO_ROOT=/path/to/where/gop-dnn-epadb-repo/use
```

## How to run

1. Run data_preparation.sh to create the necessary directories and files. This script creates soft links to wsj folders in Kaldi, downloads and extracts the acoustic and language models from kaldi web, computes mfcc's and extracts i-vectors.  

```
./data_preparation.sh
```

6. Run the run.sh script:

```
./run.sh
```

7. You will find the results in the results folder.


## How to evaluate

1. Run the evaluation script:

```
./run_eval.sh
```

3. You should expect to obtain a pickle file with all the information necessary to compute ROC, AUC, and EERs.


## References

* Hu, Wenping, Yao Qian, and Frank K. Soong. "An improved DNN-based approach to mispronunciation detection and diagnosis of L2 learners' speech." SLaTE. 2015. [link](https://www.slate2015.org/files/submissions/Hu15-AID.pdf)

* Povey, Daniel, et al. "Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks." Interspeech. 2018. [link](https://www.danielpovey.com/files/2018_interspeech_tdnnf.pdf)
