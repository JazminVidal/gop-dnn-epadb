#!/usr/bin/env bash

# This script returns wav.scp file into data folder. It takes as argument the path were the waveforms are stored. Wav.scp
# contains logid+path/to/wavs. See Kali data preparation for more information.
# The script assumes a corpus folder with a folder per speaker with wavs inside.

python generate_wav_scp.py corpus #path/to/waveforms


#The following code will extract the MFCC acoustic features
#and compute the cepstral mean and variance normalization (CMVN) stats.
#The --nj option is for the number of jobs to be sent out. This number is currently set to 8 jobs.
#It is good to note that Kaldi keeps data from the same speakers together,
#so you do not want more splits than the number of speakers you have.
#After each process, it also fixes the data files to ensure that they are still in the correct format.


datadir=test_epa

steps/make_mfcc.sh --nj 20 --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" data/${datadir}_hires
steps/compute_cmvn_stats.sh data/${datadir}_hires
utils/fix_data_dir.sh data/${datadir}_hires

#Extracting i-vectors
#the i-vector extractor to obtain i-vectors for our data
#This will extract 100-dim i-vectors to exp/nnet3_cleaned
utils/copy_data_dir.sh data/$datadir data/${datadir}_hires

data=test_epa
nspk=$(wc -l <data/${data}_hires/spk2utt)
steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj "${nspk}" data/${data}_hires exp/nnet3_cleaned/extractor exp/nnet3_cleaned/ivectors_${data}_hires
