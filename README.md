# # Kaldi GOP-DNN on Epa-DB


This project computes Kaldi GOP-DNN algorithm on Epa-DB, a database of non-native English speech by Spanish speakers from Argentina, using a TDNN-F chain acoustic model with iVectors downloaded from Kaldi web.

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
Epa-DB, is a database of non-native English speech by argentinian speakers of Spanish. It is intended for research on mispronunciation detection
and development of pronunciation assessment systems.
The database includes recordings from 50 non-native speakers of English, 25 male and 25 female, whose first language (L1) is Spanish from Argentina (mainly Rio de la Plata).
Each speaker recorded 64 short Englsh phrases phonetically balanced and specifically designed to globally contain all the sounds difficult to pronounce for the target population.
All recordings were forced aligned using the Montreal Forced Aligner and annotated at phone level by two expert raters.
For the sake of simplicity we followed, when possible, the organization given by the L2-ARCTIC corpus.

## Database Overview
For each speaker, the database contains:

* **Speech recordings**: 64 short English phrases (some of them may have been removed because of quality problems)
* **Word level transcriptions**: orthographic transcription and forced-aligned word boundaries provided by Montreal Forced Aligner.
* **Phoneme level transcriptions**: ARPA-bet transcriptions provided by Montral Forced Aligner with manually corrected boundaries by the raters.
* **Manual annotations**: phone level annotations in ARPA-bet and an ARPA-bet like extension to account for those sounds not present in the English inventory.
* **Reference transcriptions**: for each utterance, the set of all the correct pronunciations in ARPA-bet. This file is useful to compute labels.

For more information on the database, please go to the [documentation](https:) or [publication](https://www.isca-speech.org/archive/Interspeech_2019/abstracts/1839.html)

## Prerequisites
1. If not already done, download and install Kaldi (http://kaldi-asr.org/).
As suggested during the installation, do not forget to add the path of the Kaldi binaries into $HOME/.bashrc

2. Download Epa-DB from (). The folder contains the subsample of 30 speakers, 15 male and 15 female, necessary to run this experiment. Each directory contains waveforms and transcripts. Put it under kaldi/egs/epadb

3. Download Librispeech ASR model from https://kaldi-asr.org/models/m13


## How to install
To install this repository, do the following steps:

1. Make sure all the recommendations in the “Prerequisites” sections are installed, correctly working or complete.

2. Clone the epadb repository:
```
git clone https://github.com/JazminVidal/epadb.git
```
3. Move epadb to kaldi/egs

4. Enter the new directory epadb in kaldi/egs and make soft links to the directories steps, utils, and src
in the wsj directory in Kaldi to access necessary scripts:

```
cd epdab

ln -s ../wsj/s5/steps .
ln -s ../wsj/s5/utils .
ln -s ../../src .

```

5. Change the KALDI_ROOT in the path.sh file to your KALDI-TRUNK:

```
# Change the path line in path.sh from:
export KALDI_ROOT='pwd'/../../..
# to:
export KALDI_ROOT=path/to/where/your/kaldi-trunk/is

```

6. Open Librispeech ASR model in kaldi/egs/epadb

7. Move the folder tdnn_1d_sp in kaldi/egs/epadb/0013_librispeech_v1/exp/chain_cleaned/tdnn_1d_sp to kaldi/egs/epadb/exp/nnet3_cleaned. The following command should work:

```
mv tdnn_1d_sp/ ../../../exp/nnet3_cleaned
```
8. Uncompress data.zip folder 

9. Move the lang_chain folder in data/lang_chain to kaldi/egs/epadb/0013_librispeech_v1/data/lang to kaldi/egs/epadb/data

```
mv lang_chain ../../../data
```


10. Your directory should now look something like this:



## How to run

1. Run prepare_data.sh to create wav.scp file, compute features and extract i-vectors:

```
bash prepare_data.sh
```

2. Replace the run.sh file in kaldi/egs/gop/s5 with the one provided in the misc folder in this repository

3. Replace make_test_case.sh kaldi/egs/gop/s5/local with the one provided in the misc folder in this repository

4. Go to kaldi/egs/gop/s5 and run the run.sh script:

```
./run.sh
```

## How to evaluate

## References

* Hu, Wenping, Yao Qian, and Frank K. Soong. "An improved DNN-based approach to mispronunciation detection and diagnosis of L2 learners' speech." SLaTE. 2015. [link](https://www.slate2015.org/files/submissions/Hu15-AID.pdf)*

* Povey, Daniel, et al. "Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks." Interspeech. 2018. [link](https://www.danielpovey.com/files/2018_interspeech_tdnnf.pdf)*

