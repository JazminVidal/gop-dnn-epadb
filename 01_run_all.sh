#!/usr/bin/env bash -e


stage=1

head=original  # original or xent
normtype=norm  # max or norm


if [ $stage -le 1 ]; then
  ./02_data_preparation.sh $head $normtype
fi

if [ $stage -le 2 ]; then
  ./03_compute.sh $head $normtype
fi
