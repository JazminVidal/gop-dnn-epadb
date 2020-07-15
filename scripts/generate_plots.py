import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import timeit
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import brentq
from scipy import interpolate
import joblib
from IPython import embed
from sklearn.metrics import roc_curve, auc
import seaborn as sns
sns.set_context('poster')
import pandas as pd
import os
import os, errno, re
import os.path as path
import sys
import tqdm
import glob
import argparse
from IPython import embed
from pathlib import Path


def plot(scores, output_dir):

    output = []

    label_histogram1 = "GOP DNN +"
    label_histogram2 = "GOP DNN -"

    label_roc_curve = "GOP DNN"

    colum1 = "AUC GOP-DNN"
    colum3 = "EER GOP-DNN"

    # list of phones in order

    phones = sorted(scores.phone.unique())

    for phone in phones:

        tar = list(scores.loc[(scores['phone'] == phone) & (scores['label'] == 1)].gop_scores)
        non = list(scores.loc[(scores['phone'] == phone) & (scores['label'] == 0)].gop_scores)

        labels_tar = list(scores.loc[(scores['phone'] == phone) & (scores['label'] == 1)].label)
        labels_non = list(scores.loc[(scores['phone'] == phone) & (scores['label'] == 0)].label)

        all = tar + non
        labels = labels_tar + labels_non

        if len(tar) >= 1 and len(non) >= 1:

            fpr, tpr, _ = roc_curve(labels, all)
            roc_auc = auc(fpr, tpr)
            eer = brentq(lambda x: 1. - x - interpolate.interp1d(fpr, tpr)(x), 0., 1.)

            output.append({'phone': phone,
                            'auc': roc_auc,
                            'eer': eer,
                            'cant +': str(len(tar)),
                            'cant -': str(len(non)),
                            })

            fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(20,10))
            fig.suptitle("Phone: "+str(phone), fontsize=30)
            lw = 2

            ax1.plot(fpr, tpr, color='darkorange',label=label_roc_curve+' (AUC = %0.2f ' % roc_auc + ' EER =  %0.2f '%eer+')')
            ax1.legend()
            ax1.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

            
            sns.kdeplot(tar,color='b',label=label_histogram1, bw=1.5)
            sns.kdeplot(non,color='g',label=label_histogram2, bw=1.5)
            ax2.legend()

            fig.savefig(output_dir + '/' + 'ROC_plot' + phone + '.pdf')
            plt.show()

        else:
            print("Unplotted phone  "+str(phone))


def main(args):

    scores = joblib.load(args.data_for_eval + 'data_for_eval.pickle')
    plots = plot(scores, args.output_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--data-for-eval-dir', dest='data_for_eval', help='Dir where data_for_eval.pickle is', default=None)
    parser.add_argument('--output-dir', dest='output_dir', help='Output dir', default=None)

    args = parser.parse_args()
    main(args)
