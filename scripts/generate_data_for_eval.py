#!/usr/bin/env python
# coding: utf-8

import os, errno, re
import os.path as path
from os import remove
import numpy as np
import textgrids # pip install git+https://github.com/Legisign/Praat-textgrids
from scipy.stats.stats import pearsonr
from IPython import embed
import pandas as pd
import joblib
import shutil
import argparse
import glob
import csv




class ScoreParam:

    def __init__(self, gap, mismatch):
        self.gap = gap
        self.mismatch = mismatch
    def match(self, chr):
        if chr == 'A':
            return 3
        elif chr == 'C' or chr == 'T':
            return 2
        else:
            return 1


def interchangeable(phone1, phone2, possible_prons_dic):
	return phone1 in possible_prons_dic.keys() and phone2 in possible_prons_dic[phone1]


def global_align(x, y, possible_prons_dic, score=ScoreParam(-4, -3)):

    A = []
    for i in range(len(y) + 1):
        A.append([0] * (len(x) +1))
    for i in range(len(y)+1):
        A[i][0] = score.gap * i
    for i in range(len(x)+1):
        A[0][i] = score.gap * i
    for i in range(1, len(y) + 1):
        for j in range(1, len(x) + 1):

            A[i][j] = max(
            A[i][j-1] + score.gap,
            A[i-1][j] + score.gap,
            A[i-1][j-1] + (score.match(y[i-1]) if y[i-1] == x[j-1] else score.mismatch)
            )
    align_X = ""
    align_Y = ""

    i = len(x)
    j = len(y)

    while i > 0 or j > 0:

        current_score = A[j][i]

        if i > 0 and j > 0 and (x[i - 1] == y[j - 1] or interchangeable(x[i - 1], y[j - 1], possible_prons_dic)):
            #embed()
            align_X = x[i - 1] + ' ' + align_X
            align_Y = y[j - 1] + ' ' + align_Y
            i = i - 1
            j = j - 1

        elif i > 0 and (current_score == A[j][i - 1] + score.mismatch or current_score == A[j][i - 1] + score.gap):
            align_X = x[i - 1] + ' ' + align_X
            align_Y = "-" + ' ' + align_Y
            i = i - 1

        else:
            align_X = "-" + ' ' + align_X
            align_Y = y[j - 1] + ' ' + align_Y
            j = j - 1

    return (align_X, align_Y)






def phonelist2str(phones):
    return " ".join(["%3s"%p for p in phones])

# Function that matches phone ints to phone symbols and loads them to a dictionary

def phones2dic(path):
    phones_dic = {}
    with open(path, "r") as fileHandler:
        line = fileHandler.readline()
        while line:
            l=line.split()
            phones_dic[int(l[1])] = l[0]
            line = fileHandler.readline()

    return phones_dic


def mkdirs(newdir):
    try: os.makedirs(newdir)
    except OSError as err:
        # Raise the error unless it's about an already existing directory
        if err.errno != errno.EEXIST or not os.path.isdir(newdir):
            raise


def get_possible_prons(possible_prons_path):
	possible_prons_dic = dict()
	with open(possible_prons_path, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			target= row[0]
			allophone = row[1]
		
			if target in possible_prons_dic.keys():
				allophones = possible_prons_dic[target]
			else:
				allophones = []

			allophones.append(allophone)
			possible_prons_dic[target] = allophones


	return possible_prons_dic

def get_reference(file):
    reference = []
    annot_manual = []
    labels = []
    i = 0
    for line in open(file).readlines():
        l=line.split()
        reference.append(l[1])
        annot_manual.append(l[2])
        labels.append(l[3])

        i += 1

    return reference, annot_manual, labels




# Function that reads the output of gop-dnn and returns the
# phone alignments

def get_gop_alignments(path_filename, phone_pure_dic):

    output = []
    for line in open(path_filename).readlines():
        l=line.split()

        if len(l) < 2:
            print("Invalid line")
        else:
            logid = l[0].replace("'", "")
            data = l[1:]
            i = 0
            phones = []
            gops = []
            phones_name = []
            while i < len(data):
                if data[i] == "[":
                    phone = int(data[i+1])
                    phone_name = phone_pure_dict[phone]

                    if phone_name not in ('SIL', 'sil', 'sp', 'spn', 'SP', 'SPN'):
                        gop = float(data[i+2])
                        phones.append(phone)
                        gops.append(gop)
                        phones_name.append(phone_name)


                    i = i + 4

            output.append({'logid': str(logid),
                            'phones': phones,
                           'phones_name':phones_name,
                           'gops':gops})

    df_phones = pd.DataFrame(output).set_index("logid")

    return df_phones


# Function that matches labels and phones from manual annotations with phones and scores from gop-dnn.
# This is a necessary step because manual annotations based on the forced alignments
# do not always coincide with gop's alignments.
# Note that whenever a phone is missing in the gop alignment a "?" is added to discard the corresponding label
# and, whenever a '0' (deletion) is present in the manual annotation, the gop score is discarded.

def match_labels2gop(logid, trans_zero, trans_manual, trans_auto, labels, gop_scores):

    output_ = []
    rows = []
    j = 0

    for i in range(0, len(trans_manual)):

        label = 0
        if(labels[i] == '+'):
            label = 1

        phone_manual = trans_manual[i]
        phone_zero = trans_zero[i]

        if phone_zero != '0' and phone_zero != '-':
            if j > len(trans_auto)-1:
                raise Exception("Index out of range")

            phone_automatic = trans_auto[j]
            rows.append([logid, phone_automatic, label, gop_scores[j]])
            j = j + 1

    columns = ['logid', 'phone', 'label', 'gop_scores']
    df = pd.DataFrame(rows, columns=columns)
    return df


def get_labels(trans_reff_complete, annot_manual, possible_prons_dic):
	labels = []
	for i in range(0, len(trans_reff_complete)):
		phone_reference = trans_reff_complete[i]
		phone_manual = annot_manual[i]

		if phone_reference == phone_manual or (phone_reference in possible_prons_dic.keys() and phone_manual in possible_prons_dic[phone_reference]):
			label = '+'
		else:	
			label = '-'

		labels.append(label)

	return labels	

# Function that reads transcriptions files and loads them to
# a series of useful dictionaries

def generate_dict_from_transcripctions(transcriptions):

    sent_dict = dict()

    # Read transcription file
    for line in open(transcriptions,'r'):

        fields = line.strip().split()

        if len(fields) <= 2:
            continue

        sent = fields[1].strip(":")

        if fields[0] == "TEXT":
            sent_dict[sent] = fields[2:]

        if fields[0] != "TRANSCRIPTION":
            continue


    return sent_dict



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--transcription-file', dest='transcriptions', help='File with reference phonetic transcriptions of each of the phrases', default=None)
    parser.add_argument('--output-dir', dest='output_dir', help='Output dir', default=None)
    parser.add_argument('--gop-file', dest='gop_path', help='File with gop results', default=None)
    parser.add_argument('--phones-pure-file', dest='phones_pure_path', help='file that matches phone ints to phone symbols', default=None)
    parser.add_argument('--reference-file', dest='reference_path', help='', default=None)
    parser.add_argument('--possible-prons-kaldi', dest='possible_prons_path_kaldi', help='', default=None)



    args = parser.parse_args()

    # Code that generates a pickle with useful data to analyze.
    # The outpul will be used to compute ROCs, AUCs and EERs.

    output = []
    possible_prons_kaldi_dic = get_possible_prons(args.possible_prons_path_kaldi)

    phone_pure_dict = phones2dic(args.phones_pure_path)
    gop_alignments = get_gop_alignments(args.gop_path, args.phones_pure_path)


    sent_dict = generate_dict_from_transcripctions(args.transcriptions)
    utterance_list = [re.sub('.txt','', re.sub('.*\/','',s)) for s in glob.glob("%s/*/labels/*.txt"%args.reference_path)]
    # Now, iterate over utterances


    for utterance in utterance_list:

        spk, sent = utterance.split("_")
        #tgfile = "%s/%s/%s.TextGrid"%(args.labels_dir, spk, utterance) #TextGrid file for current utterance

        file = "%s/%s/%s/%s.txt"%(args.reference_path, spk, "labels", utterance) #TextGrid file for current utterance
        print("----------------------------------------------------------------------------------------")
        print("Speaker %s, sentence %s: %s (File: %s)"%(spk, sent, " ".join(sent_dict[sent]), file))
        
        #Get phone list from manual annotation 
        trans_reff_complete, annot_manual, labels = get_reference(file)


        if utterance in gop_alignments.index.values:
            phone_idxs = gop_alignments.loc[utterance].phones
            gop_scores = gop_alignments.loc[utterance].gops
            annot_kaldi = []
            for phone_idx in phone_idxs:
                phone = phone_pure_dict[phone_idx]
                if phone not in ['sil', '[key]', 'sp', '', 'SIL', '[KEY]', 'SP']:
                    if phone[-1] not in ['1', '0', '2']:
                        annot_kaldi += [phone]
                    else:

                        # If it has an int at the end, delete it, except for AH0

                        annot_kaldi += [phone] if(phone == 'AH0') else [phone[:-1]]
        else:

            raise Exception("WARNING: Missing score for "+ utterance)

        align = global_align(annot_manual, annot_kaldi, possible_prons_kaldi_dic, score=ScoreParam(-4, -3))
        trans_zero= align[1].strip().split(' ')

        print("TRANS_MANUAL:         "+phonelist2str(annot_manual))
        print("TRANS_KALDI:          "+phonelist2str(annot_kaldi))
        print("TRANS_ZERO:           "+phonelist2str(trans_zero))
        print("TRANS_REFF_COMPLETE:  "+phonelist2str(trans_reff_complete))
        print("LABEL:                "+phonelist2str(labels))

        outdir  = "%s/labels/%s" % (args.output_dir, spk)
        outfile = "%s/%s.txt" % (outdir, utterance)
        mkdirs(outdir)

        annot_manual_align = align[1].strip().split(' ')
        
        if len(annot_manual_align) != len(annot_manual):
            raise Exception("WARNING: different lengths")
        else: 

            df = match_labels2gop(utterance, trans_zero, annot_manual, annot_kaldi, labels, gop_scores)
            output.append(df)


    df_trans_match = pd.concat(output).set_index('logid')

    #Export file containing data for evaluation

    joblib.dump(df_trans_match, args.output_dir + '/data_for_eval.pickle')
