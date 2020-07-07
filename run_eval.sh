#!/bin/sh

set -ex

python3 generate_data_for_eval.py  \
		--trans-SAE-path 'gop_files/transcriptionsSAE.txt'  \
		--trans-complete-path 'gop_files/trans_complete.txt'  \
		--textgrids-list 'manual_annot/textgrid_list' \
		--gop-path 'gop_files/gop.1.txt' \
		--phones-pure-path 'gop_files/phones-pure.txt' \
	  	--manual-annot-dir 'manual_annot' \
	  	--export-path 'results'  \
		--log-dir 'logs'  \
