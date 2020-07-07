export KALDI_ROOT=/Users/jazmin/Desktop/kaldi
export EPADB_ROOT=/Users/jazmin/Desktop/epadb
export GOPEPA_REPO_ROOT=/Users/jazmin/Desktop/gop-dnn-epadb

[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh

export PATH=$KALDI_ROOT/egs/wsj/s5/utils:$KALDI_ROOT/egs/wsj/s5/step:$KALDI_ROOT/egs/gop/s5/local:$KALDI_ROOT/tools/openfst/bin:$PATH

[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1

. $KALDI_ROOT/tools/config/common_path.sh

export LC_ALL=C
