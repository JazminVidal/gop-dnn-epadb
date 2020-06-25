#!/bin/sh

#set -x

echo "preparing epadb directories"

. ./path.sh

ln -s $KALDI_ROOT/egs/wsj/s5/steps .
ln -s $KALDI_ROOT/egs/wsj/s5/utils .
ln -s $KALDI_ROOT/src .

# The script takes epadb waveforms and transcriptions and creates a temporal directory with .wav and .lab files to extract features.
# In the end you should expect to have wav.scp, utt2spk, spk2utt and text file in data/test folder.

# Aca la carpeta data es una carpeta temporal que apunta a $EPADB_ROOT y saca los wavs y los labs de cada speaker y los ordena como estaba ordenada
# corpus.
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

# Move folders to the corresponding directories
cp -r 0013_librispeech_v1/exp/chain_cleaned/tdnn_1d_sp exp/nnet3_cleaned
cp -r 0013_librispeech_v1/exp/nnet3_cleaned/extractor exp/nnet3_cleaned
cp -r 0013_librispeech_v1/data/lang_chain data/


# feature extraction
utils/copy_data_dir.sh data/test_epa data/test_epa_hires

echo "Extracting features for DNN model!"
steps/make_mfcc.sh --nj 8 --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" data/test_epa_hires
steps/compute_cmvn_stats.sh data/test_epa_hires
utils/fix_data_dir.sh data/test_epa_hires


# Extract ivectors
nspk=$(wc -l <data/test_epa_hires/spk2utt)
steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj "${nspk}" data/test_epa_hires exp/nnet3_cleaned/extractor exp/nnet3_cleaned/ivectors_test_epa_hires

echo "Finish data preparation and feature extraction!"

#echo "prepareing GOP directories" # Quizas esta parte deberia estar en el run.sh

# Aca hay que ponerle el path absoluto para que lo mande a dobde la persona tenga KALDI_ROOT segun path.sh
gop_dir='../gop/s5'
mkdir $gop_dir/exp
mkdir $gop_dir/data
cp -r data/test_epa_hires $gop_dir/data/
mv $gop_dir/data/test_epa_hires $gop_dir/data/test_epa
