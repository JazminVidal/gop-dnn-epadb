#!/usr/bin/env python
# coding: utf-8

# This script returns wav.scp file into data folder. It takes as argument the path were the waveforms are stored. Wav.scp
# contains logid+path/to/wavs. See Kali data preparation for more information.

from pathlib import Path
from glob import glob
import os
import joblib
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('wavs_path', help='path a wavs', default=None)
    args = parser.parse_args()
    with open('data/test_epa/wav.scp','w') as fp:
        for file in sorted(glob(args.wavs_path+'/*/*.wav')):
            fp.write('{} {}\n'.format(Path(file).stem,Path(file).absolute()))
