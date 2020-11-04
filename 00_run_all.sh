#!/usr/bin/env bash -e

stage=${1:-1}
stage=3

head=original  # original or xent
normtype=norm  # max or norm

if [ $stage -le 1 ]; then
  ./01_recompile.sh
fi

if [ $stage -le 2 ]; then
  ./02_data_preparation.sh $head $normtype
fi

if [ $stage -le 3 ]; then
  ./03_compute.sh $head $normtype
fi
