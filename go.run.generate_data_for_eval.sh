#!/bin/sh

set -ex

python3 generate_data_for_eval.py  \
		--trans-SAE-path 'transcriptionsSAE.txt'  \
		--trans-complete-path 'trans_complete.txt'  \
		--textgrids-list 'textgrid_list' \
		--gop-path 'gop.1.txt' \
		--phones-pure-path 'phones-pure.txt' \
	  --labels-dir 'labels_dir' \
	  --export-path 'results'  \
		--log-dir 'log_dir'  \
