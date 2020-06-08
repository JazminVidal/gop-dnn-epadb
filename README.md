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
1. Kaldi: (http://kaldi-asr.org/).

2. Epa-DB: (). You will be using in this experiment a subsample of 30 speakers, 15 male and 15 female.

3. Librispeech ASR model: https://kaldi-asr.org/models/m13

4. TextGrid managing library: https://github.com/Legisign/Praat-textgrids


## How to install
To install this repository, do the following steps:

1. If not already done, download and install Kaldi. As suggested during the installation, do not forget to add the path of the Kaldi binaries into $HOME/.bashrc

3. Clone the epadb repository into kaldi/egs/:
```
git clone https://github.com/JazminVidal/epadb.git
```

3. Check the requirements.txt file:
```
pip install -r requirements.txt
```

4. Change the KALDI_ROOT in the path.sh file to your KALDI-TRUNK:
```
# Change the path line in path.sh from:
export KALDI_ROOT='pwd'/../../..
# to:
export KALDI_ROOT=path/to/where/your/kaldi-trunk/is
```

5. Your epadb directory inside Kaldi should now look something like this:



## How to run

1. Download epa-db corpus folder into kaldi/egs/epadb.

2. Run data_preparation.sh to create the necessary directories and files. This script creates soft links to wsj folders in Kaldi, downloads and extracts the acoustic and language models from kaldi web, computes mfcc's and extracts i-vectors.  

```
./data_preparation.sh
```

3. After running data_preparation.sh, go to kaldi/egs/gop/s5

4. Replace make_test_case.sh in kaldi/egs/gop/s5/local and run.sh in kaldi/egs/gop/s5 with the ones provided in the misc folder in this repository. 

5. Change the path.sh in kaldi/egs/gop/s5 so that the paths needed match your own paths.

6. Run the run.sh script:

```
./run.sh
```

7. You will find the reuslts in the exp folder. 


## How to evaluate

1. Move the gop.1.txt file resulting from running kaldi/gop recipe for Epa-DB to kaldi/egs/epadb/evaluation 

2. Run the evaluation script:

```
./go.run.generate_data_for_eval.sh
```
3. You should expect to obtain a pickle file with all the information necessary to compure ROC, AUC, and EERs. 


## References

* Hu, Wenping, Yao Qian, and Frank K. Soong. "An improved DNN-based approach to mispronunciation detection and diagnosis of L2 learners' speech." SLaTE. 2015. [link](https://www.slate2015.org/files/submissions/Hu15-AID.pdf)

* Povey, Daniel, et al. "Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks." Interspeech. 2018. [link](https://www.danielpovey.com/files/2018_interspeech_tdnnf.pdf)

