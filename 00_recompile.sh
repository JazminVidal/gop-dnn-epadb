#!/bin/bash -e

echo "Recompiling Kaldi with new compute-gop.cc"

. ./path.sh

cd $KALDI_ROOT/src/bin
make
