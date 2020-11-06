# Kaldi GOP-DNN on Epa-DB

This repository has the tools to run a Kaldi-based GOP-DNN algorithm on Epa-DB, a database of non-native English speech by Spanish speakers from Argentina. It uses a TDNN-F chain model which is downloaded from the Kaldi website and Kaldi's official GOP-DNN recipe.

It also provides a modified version of Kaldi's compute-gop.cc binary that allows to compute to different types of normalizations plus a modified version of the TDNN-F model that uses a different head. Both, head and normalization type, are set as parameters in the 01_run.sh script.

If you use this code or the Epa database, please cite the following paper:

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
* [Notes on Kaldi-DNN-GOP](#Notes-on-Kaldi-DNN-GOP)
* [References](#references)


## Introduction

This toolkit is meant to facilitate experimentation with Epa-DB by allowing users to run a state-of-the-art baseline system on it.
Epa-DB, is a database of non-native English speech by argentinian speakers of Spanish. It is intended for research on mispronunciation detection
and development of pronunciation assessment systems.
The database includes recordings from 50 non-native speakers of English, 25 male and 25 female, whose first language (L1) is Spanish from Argentina (mainly of the Rio de la Plata dialect).
Each speaker recorded 64 short English phrases phonetically balanced and specifically designed to globally contain all the sounds difficult to pronounce for the target population.
All recordings were annotated at phone level by expert raters.

For more information on the database, please refer to the [documentation]() or [publication]()

If you are only looking for the EpaDB corpus, you can download it from this [link](https://www.dropbox.com/s/hnbjcaloag6pumc/epadb_30.zip?dl=0).

## Prerequisites

1. [Kaldi](http://kaldi-asr.org/) installed.

2. TextGrid managing library installed using pip. Instructions at this [link](https://pypi.org/project/praat-textgrids/).

3. [The EpaDB database](https://www.dropbox.com/s/hnbjcaloag6pumc/epadb_30.zip?dl=0) downloaded.

4. [Librispeech ASR model](https://kaldi-asr.org/models/m13)

5. [Librispeech ASR model Xent head](https://www.dropbox.com/s/u0mp49e9kuwjbxe/final_xent.mdl?dl=0)


## How to install

To install this repository, do the following steps:

1. Clone this repository:
```
git clone https://github.com/JazminVidal/gop-dnn-epadb.git
```

2. Download Librispeech ASR acoustic model from Kaldi and move it or link it inside the top directory of the repository:

```
wget https://kaldi-asr.org/models/13/0013_librispeech_s5.tar.gz
tar -zxvf 0013_librispeech_s5.tar.gz
```

3. go to 0013_librispeech_v1/exp/chain_cleaned/tdnn_1d_sp and change final.mdl name to final_original.mdl


4. Download Librispeech ASR Xent acoustic model from the link in prerequisites and move it to 0013_librispeech_v1/exp/chain_cleaned/tdnn_1d_sp


5. Install the requirements:

```
pip install -r requirements.txt
```

6. Set the following lines in the file path.sh inside the repository's top directory:

Path to Epa-DB should be an absolute path.

```
export KALDI_ROOT=path/to/where/your/kaldi-trunk/is
export EPADB_ROOT=path/to/where/epadb/is
export MODEL_ROOT=path/to/where/final.mdl/is
```

7. Move compute-gop.cc file to kaldi/src/bin/


8. Run 00_recompile.sh


## How to run


1. Run 

```
01_run_all.sh 
```

to create the necessary directories and files. This script calls 02_data_preparation.sh that creates soft links to wsj folders in Kaldi, downloads and extracts the acoustic and language models from kaldi web, computes mfcc's, extracts i-vectors and creates temporary folders from Epa-DB files and calls 03_compute.sh that 
computes alignments and goodness of pronunciation scores and stores the results under the exp_epadb/test folder. Results include alignments, files with the posteriors from the DNN (in probs), and files with the final gop scores (in gop). The script computes labels for Epa-DB by comparing the manual annotations in annotations_1 to all the possible reference transcriptions in the trans_complete file, aligning the resulting labels to the gop scores. Results are stored under exp_epadb/test/gop_with_labels folder. Finally, the script generates a folder with ROC curves for each phone.



## Notes on Kaldi-DNN-GOP

Notes adapted from run.sh file in Kaldi DNN-GOP official recipe:

1. The outputs of the binary compute-gop are the GOPs and the phone-level features (which we are not using). An example of the GOP result looks like:

                    4446-2273-0031 [ 1 0 ] [ 12 0 ] [ 27 -5.382001 ] [ 40 -13.91807 ] [ 1 -0.2555897 ] \
                                  [ 21 -0.2897284 ] [ 5 0 ] [ 31 0 ] [ 33 0 ] [ 3 -11.43557 ] [ 25 0 ] \
                                  [ 16 0 ] [ 30 -0.03224623 ] [ 5 0 ] [ 25 0 ] [ 33 0 ] [ 1 0 ]

Results are in posterior format, where each pair stands for [pure-phone-index gop-value]. For example, [ 27 -5.382001 ] means the GOP of the pure-phone 27 (which corresponds to the phone "OW", according to "phones-pure.txt") is -5.382001.

2. The phone-level features are in matrix format:

                   4446-2273-0031  [ -0.2462088 -10.20292 -11.35369 ...
                                     -8.584108 -7.629755 -13.04877 ...
                                     ...
                                     ... ]


## References

* Hu, Wenping, Yao Qian, and Frank K. Soong. "An improved DNN-based approach to mispronunciation detection and diagnosis of L2 learners' speech." SLaTE. 2015. [link](https://www.slate2015.org/files/submissions/Hu15-AID.pdf)

* Povey, Daniel, et al. "Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks." Interspeech. 2018. [link](https://www.danielpovey.com/files/2018_interspeech_tdnnf.pdf)

* Kaldi DNN-GOP official recipe by Junbo Zhang https://github.com/kaldi-asr/kaldi/tree/master/egs/gop
