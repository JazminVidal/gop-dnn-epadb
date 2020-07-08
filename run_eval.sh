#!/bin/sh

set -ex

. ./path.sh

python3 generate_data_for_eval.py  \
		--trans-SAE-path $EPADB_ROOT/transcriptionsSAE.txt  \
		--trans-complete-path $EPADB_ROOT/trans_complete.txt  \
		--textgrids-list 'textgrid_list' \
		--gop-path 'exp/gop_test_epa_hires/gop.1.txt' \
		--phones-pure-path 'exp/gop_test_epa_hires/phones-pure.txt' \
	  --manual-annot-dir 'labels_dir' \
	  --export-path 'results'  \
		--log-dir 'logs'  \
