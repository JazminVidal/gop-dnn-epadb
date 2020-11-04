#!/usr/bin/env bash -e

echo "Recompiling Kaldi with new compute-gop.cc"

cd $KALDI_ROOT/src/bin
make
