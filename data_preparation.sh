#!/bin/sh

#set -x

echo 'Preparing useful directories'

. ./path.sh

ln -s $KALDI_ROOT/egs/wsj/s5/steps .
ln -s $KALDI_ROOT/egs/wsj/s5/utils .
ln -s $KALDI_ROOT/src .

# The script takes epadb waveforms and transcriptions and creates a temporal directory with .wav and .lab files to extract features.
# In the end you should expect to have wav.scp, utt2spk, spk2utt and text file in data/test folder.


echo 'Creating epadb corpus folder from epadb files'

[ ! -d corpus ] && mkdir corpus
for d in $EPADB_ROOT/*/; do
    [ ! -d "corpus/$(basename $d)" ] && mkdir "corpus/$(basename $d)"
    for f in $d/waveforms/*.wav $d/transcriptions/*.lab; do
	ln -sf $f "corpus/$(basename $d)"
    done
done

data='corpus'
dir='data/test_epa'
mkdir -p $dir

echo 'Preparing data dirs'

for d in $data/*; do
    #echo $d
    for f in $d/*.wav; do
        filename="$(basename $f)"
        filepath="$(dirname $f)"
        spkname="$(basename $filepath)"
        echo "${filename%.*} $filepath/$filename" >> $dir/wav.scp # Prepare wav.scp
        echo "$spkname ${filename%.*}" >> $dir/spk2utt # Prepare spk2utt
        echo "${filename%.*} $spkname" >> $dir/utt2spk # Prepare utt2spk
        (
            printf "${filename%.*} "
            cat "$data/$spkname/${filename%.*}.lab" | tr [a-z] [A-Z]
            printf "\n"
        ) >> $dir/text # Prepare transcript
    done
done

utils/fix_data_dir.sh $dir

# wav-to-duration --read-entire-file=true p,scp:$dir/wav.scp ark,t:$dir/utt2dur || exit 1; # Prepare utt2dur

# Download language model and acoustic model from Kaldi. For more details see: https://kaldi-asr.org/models/m13

echo 'Downloading models from Kaldi'

[ ! -f 0013_librispeech_s5.tar.gz ] &&  wget https://kaldi-asr.org/models/13/0013_librispeech_s5.tar.gz
[ ! -d 0013_librispeech_v1 ] &&  tar -zxvf 0013_librispeech_s5.tar.gz

echo 'Reorganizing folders'

# Move folders to the corresponding directories

cp -r 0013_librispeech_v1/data/lang_chain data/


# copying folder for feature extraction
utils/copy_data_dir.sh data/test_epa data/test_epa_hires

echo 'Extracting features for DNN model!'

steps/make_mfcc.sh --nj 8 --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" data/test_epa_hires
steps/compute_cmvn_stats.sh data/test_epa_hires
utils/fix_data_dir.sh data/test_epa_hires

# Extract ivectors

echo 'Extracting ivectors'

#nspk=$(wc -l <data/test_epa_hires/spk2utt)
#"${nspk}"

steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj 30  \
      data/test_epa_hires 0013_librispeech_v1/exp/nnet3_cleaned/extractor \
      exp/nnet3_cleaned/ivectors_test_epa_hires

echo "Finish data preparation and feature extraction!"
