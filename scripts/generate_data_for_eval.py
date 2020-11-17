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


# Generates transcription file without allophonic variations

def generate_trans_SAE(trans_complete):

    complete_text = open(trans_complete)
    pruned_text = open("transcriptionsSAE.txt","w")

    d = [('Th/', ''), ('Kh/', ''), ('Ph/', ''), ('AX', 'AH0'), ('/DX', '')]

    s = complete_text.read()
    for i,o in d:
        s = s.replace(i,o)
    pruned_text.write(s)

    complete_text.close()
    pruned_text.close()

    return pruned_text


# Function that reads transcriptions files and loads them to
# a series of useful dictionaries

def generate_dict_from_transcripctions(transcriptions):

    trans_dict = dict()
    trans_dict_clean = dict()
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

        if sent not in trans_dict_clean:

            # Before loading the first transcription for a sentence,
            # create an entry for it in the dict. The entry will be a
            # list of lists. One list for each possible transcription
            # for that sentence.

            trans_dict[sent] = list()
            trans_dict_clean[sent] = list()

        trans = [[]]
        for i in range(2, len(fields)):
            phones = fields[i].split("/")

            # Reproduce the transcriptions up to now as many times as
            # the number of phone variations in this slot. Then, append
            # one variation to each copy.

            trans_new = []
            for p in phones:
                for t in trans:
                    t_tmp = t + [p.strip()]
                    trans_new.append(t_tmp)
            trans = trans_new

        trans_dict[sent] += trans

    for sent, trans in trans_dict.items():
        trans_clean_new = []
        for t in trans:
            trans_clean_new.append([x for x in t if x != '0'])

        if sent not in trans_dict_clean:
            trans_dict_clean[sent] = list()

        trans_dict_clean[sent] += trans_clean_new

    return trans_dict, trans_dict_clean, sent_dict


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
    position = 1

    for i in range(0, len(trans_manual)):

        label = 0
        if(labels[i] == '+'):
            label = 1

        phone_manual = trans_manual[i]
        phone_zero = trans_zero[i]

        if phone_zero != '0':
            if j > len(trans_auto)-1:
                raise Exception("Index out of range")

            phone_automatic = trans_auto[j]
            rows.append([logid, phone_automatic, label, gop_scores[j], phone_manual, position])
            position += 1

            j = j + 1

    columns = ['logid', 'phone_automatic', 'label', 'gop_scores', 'phone_manual', 'position']
    df = pd.DataFrame(rows, columns=columns)
    return df

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




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--transcription-file', dest='transcriptions', help='File with reference phonetic transcriptions of each of the phrases', default=None)
    parser.add_argument('--labels-dir', dest='labels_dir', help='Directory with textgrid files with annotations', default=None)
    parser.add_argument('--output-dir', dest='output_dir', help='Output dir', default=None)
    parser.add_argument('--gop-file', dest='gop_path', help='File with gop results', default=None)
    parser.add_argument('--phones-pure-file', dest='phones_pure_path', help='file that matches phone ints to phone symbols', default=None)
    parser.add_argument('--reference-file', dest='reference_path', help='', default=None)

    args = parser.parse_args()

    # Code that generates a pickle with useful data to analyze.
    # The outpul will be used to compute ROCs, AUCs and EERs.

    output = []
    output_tmp  = []

    trans_dict_complete, trans_dict_clean_complete, sent_dict_complete = generate_dict_from_transcripctions(args.transcriptions)
    generate_trans_SAE(args.transcriptions)
    #trans_dict, trans_dict_clean, sent_dict = generate_dict_from_transcripctions('transcriptionsSAE.txt')

    phone_pure_dict = phones2dic(args.phones_pure_path)
    gop_alignments = get_gop_alignments(args.gop_path, args.phones_pure_path)

    utterance_list = [re.sub('.TextGrid','', re.sub('.*\/','',s)) for s in glob.glob("%s/*/*"%args.labels_dir)]


    # Now, iterate over utterances
    for utterance in utterance_list:

        spk, sent = utterance.split("_")

        file = "%s/%s/%s/%s.txt"%(args.reference_path, spk, "labels", utterance) #TextGrid file for current utterance
        print("----------------------------------------------------------------------------------------")
        print("Speaker %s, sentence %s: %s (File: %s)"%(spk, sent, " ".join(sent_dict_complete[sent]), file))
        
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



        # Find the transcription for this sentence that best matches the annotation

        best_trans = -1
        best_trans_corr = 0

        for trans_idx, trans in enumerate(trans_dict_clean_complete[sent]):
            if(len(trans) == len(annot_kaldi)):
                num_correct = np.sum([t==a for t, a in np.c_[trans,annot_kaldi]])
                if num_correct > best_trans_corr:
                    best_trans_corr = num_correct
                    best_trans = trans_idx



        if best_trans != -1:


            trans      = trans_dict_clean_complete[sent][best_trans]
            trans_zero = trans_dict_complete[sent][best_trans]


            print("TRANS_REFF:           %s (chosen out of %d transcriptions)"%(phonelist2str(trans), len(trans_dict_clean_complete[sent])))
            print("TRANS_KALDI:          "+phonelist2str(annot_kaldi))
            print("LABEL:                "+phonelist2str(labels))
            print("TRANS_ZERO:           "+phonelist2str(trans_zero))
            print("TRANS_MANUAL:         "+phonelist2str(annot_manual))
            print("TRANS_REFF_COMPLETE:  "+phonelist2str(trans_reff_complete))
            print("TRANS_WITHOUT_ZERO:   "+phonelist2str(trans))

            outdir  = "%s/labels/%s" % (args.output_dir, spk)
            outfile = "%s/%s.txt" % (outdir, utterance)
            mkdirs(outdir)
            np.savetxt(outfile, np.c_[np.arange(len(annot_manual)), trans_reff_complete, annot_manual, labels], fmt=utterance+"_%s %s %s %s")

            df = match_labels2gop(utterance, trans_zero, annot_manual, annot_kaldi, labels, gop_scores)
            output.append(df)


        else:

            raise Exception("WARNING: %s does not match with transcription"%(spk))



    df_trans_match = pd.concat(output).set_index('logid')

    #Export file containing data for evaluation

    joblib.dump(df_trans_match, args.output_dir + '/data_for_eval.pickle')


