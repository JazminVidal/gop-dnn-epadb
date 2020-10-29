#!/usr/bin/env bash -e

# This script calculates Goodness of Pronunciation (GOP) scores and
# extract phone-level pronunciation feature for mispronunciations detection
# tasks for EpaDB database. The script is based in the official Kaldi GOP-dnn
# recipe.

# Make sure to run data_preparation before running this script.

. ./path.sh

# This script assumes the following paths exist.

modeldir=0013_librispeech_v1
model=$MODEL_ROOT/exp/chain_cleaned/tdnn_1d_sp
modeltype=final_original.mdl
expdir=exp_epadb/test
labels=exp_epadb/labels
ivectors=$expdir/ivectors
lang=$modeldir/data/lang_chain


for d in $model $ivectors $lang $expdir; do
  [ ! -d $d ] && echo "$0: no such path $d" && exit 1;
done

# Global configurations
stage=${1:-1}
nj=1

# Symbolic link to local folder in kaldi gop

ln -fs $KALDI_ROOT/egs/gop/s5/local

#Use selected model type for first stage
ln -fs $model/$modeltype $model/final.mdl

if [ $stage -le 1 ]; then

    echo 'Computing posteriors from the DNN'

    steps/nnet3/compute_output.sh --cmd run.pl --nj $nj \
	--online-ivector-dir $ivectors $expdir $model $expdir/probs
fi

#Use original head for all next stages
ln -fs $model/final_original.mdl $model/final.mdl

if [ $stage -le 2 ]; then

    echo 'Creating forced-alignments'

    steps/nnet3/align.sh --cmd run.pl --nj $nj --use_gpu false \
	--online_ivector_dir $ivectors $expdir $lang $model $expdir/align
fi


if [ $stage -le 3 ]; then

    echo 'Mapping phones to pure-phones'

    # make a map which converts phones to "pure-phones"
    # "pure-phone" means the phone whose stress and pos-in-word markers are ignored
    # eg. AE1_B --> AE, EH2_S --> EH, SIL --> SIL
    local/remove_phone_markers.pl $lang/phones.txt $expdir/align/phones-pure.txt $expdir/align/phone-to-pure-phone.int

    # Convert transition-id to pure-phone id
    run.pl JOB=1:$nj $expdir/log/ali_to_phones.JOB.log \
	ali-to-phones --per-frame=true $model/final.mdl "ark,t:gunzip -c $expdir/align/ali.JOB.gz|" \
	"ark,t:-" \| utils/apply_map.pl -f 2- $expdir/align/phone-to-pure-phone.int \| \
	gzip -c \>$expdir/align/ali-pure-phone.JOB.gz   || exit 1;
fi


if [ $stage -le 4 ]; then

    echo 'Computing gop'

    run.pl JOB=1:$nj $expdir/log/compute_gop.JOB.log \
	compute-gop --phone-map=$expdir/align/phone-to-pure-phone.int $model/final.mdl \
	"ark,t:gunzip -c $expdir/align/ali-pure-phone.JOB.gz|" \
	"ark:$expdir/probs/output.JOB.ark" \
	"ark,t:$expdir/gop.JOB.txt" "ark,t:$expdir/phonefeat.JOB.txt"   || exit 1;

    echo "Done computing gop, results are in: $expdir/gop.<JOB>.txt in posterior format (see Readme file)."

    cat $expdir/gop.*.txt > $expdir/gop.txt
fi


if [ $stage -le 5 ]; then

    python3 scripts/generate_data_for_eval.py  \
        --transcription-file $EPADB_ROOT/reference_transcriptions.txt  \
        --gop-file $expdir/gop.txt \
        --phones-pure-file $expdir/align/phones-pure.txt \
        --labels-dir $labels \
        --output-dir $expdir/gop_with_labels > $expdir/log/create_labels

fi


if [ $stage -le 6 ]; then

    python3 scripts/generate_plots.py  \
        --data-for-eval-dir $expdir/gop_with_labels/ \
        --output-dir $expdir/plots

    echo "Done plotting ROCs and histograms, results are in: $expdir/gop_with_labels"

fi
