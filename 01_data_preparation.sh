#!/bin/sh -e

. ./path.sh

ln -fs $KALDI_ROOT/egs/wsj/s5/steps .
ln -fs $KALDI_ROOT/egs/wsj/s5/utils .
ln -fs $KALDI_ROOT/src .

data=exp_epadb
head=original
normtype=max
expdir=$data/test_${normtype}_$head

# This script takes epadb waveforms and transcriptions and creates a temporal directory with .wav and .lab files to extract features.
# In the end you should expect to have wav.scp, utt2spk, spk2utt and text files in data/test folder.

echo 'Creating temporary folders for epadb files'

for d in $EPADB_ROOT/*/; do
    echo $d
    mkdir -p $data/corpus/$(basename $d) $data/labels/$(basename $d)
    ln -sf $d/waveforms/*.wav          $data/corpus/$(basename $d)/
    ln -sf $d/transcriptions/*.lab     $data/corpus/$(basename $d)/
    ln -sf $d/annotations_1/*.TextGrid $data/labels/$(basename $d)/
done


# Files needed by Kaldi scripts

echo 'Preparing data dirs'

mkdir -p $expdir
rm -rf $expdir/{wav.scp,spk2utt,utt2spk,text}
for d in $data/corpus/*; do

    for f in $d/*.wav; do
        filename=$(basename $f .wav)
        filepath=$(dirname $f)
        spkname=$(basename $filepath)
        echo "$filename $f"       >> $expdir/wav.scp # Prepare wav.scp
        echo "$spkname $filename" >> $expdir/spk2utt # Prepare spk2utt
        echo "$filename $spkname" >> $expdir/utt2spk # Prepare utt2spk
        (
            printf "$filename "
            cat $data/corpus/$spkname/${filename%.*}.lab | tr [a-z] [A-Z]
            printf "\n"
        ) >> $expdir/text # Prepare transcriptions
    done
done
utils/fix_data_dir.sh $expdir



# Extract the MFCC features for all the wavs

echo 'Extracting features'

steps/make_mfcc.sh --nj 2 --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" $expdir
steps/compute_cmvn_stats.sh $expdir
utils/fix_data_dir.sh $expdir

# Extract ivectors

echo 'Extracting ivectors'

steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj 30  \
    $expdir 0013_librispeech_v1/exp/nnet3_cleaned/extractor \
    $expdir/ivectors

echo 'Finished data preparation and feature extraction!'
