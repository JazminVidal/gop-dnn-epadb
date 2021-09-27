import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
from scipy import interpolate
import joblib
from sklearn.metrics import roc_curve, auc
import pandas as pd
import os, errno, re
import sys
import argparse

def mkdirs(newdir):
    try: os.makedirs(newdir)
    except OSError as err:
        # Raise the error unless it's about an already existing directory
        if err.errno != errno.EEXIST or not os.path.isdir(newdir):
            raise

def plot(scores, output_dir):

    # list of phones in order
    phones = sorted(scores.phone_automatic.unique())

    for phone in phones:

        pos = scores[(scores.phone_automatic == phone) & (scores.label == 1)]
        neg = scores[(scores.phone_automatic == phone) & (scores.label == 0)]

        pos_scores = list(pos.gop_scores)
        neg_scores = list(neg.gop_scores)

        pos_labels = list(pos.label)
        neg_labels = list(neg.label)

        all_scores = pos_scores + neg_scores
        all_labels = pos_labels + neg_labels

        if len(pos_scores) >= 50 and len(neg_scores) >= 50:

            fpr, tpr, _ = roc_curve(all_labels, all_scores)
            roc_auc = auc(fpr, tpr)
            eer = brentq(lambda x: 1. - x - interpolate.interp1d(fpr, tpr)(x), 0., 1.)

            print("Plotting phone %2s, AUC = %.2f, EER = %.2f, num_correct = %d, num_incorrect = %d"%(phone, roc_auc, eer, len(neg_scores), len(pos_scores)))

            fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(20,10))
            fig.suptitle("Phone: "+str(phone), fontsize=15)

            ax1.plot(fpr, tpr, color='darkorange',label='AUC = %0.2f, EER =  %0.2f '%(roc_auc, eer))
            ax1.legend()
            ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            ax1.set_xlabel("False Positive Rate")
            ax1.set_ylabel("True Positive Rate")

            h, e = np.histogram(all_scores, bins=40)
            c = (e[:-1]+e[1:])/2 # centros de los bins

            ht, _ = np.histogram(pos_scores, bins=e, density=True)
            hn, _ = np.histogram(neg_scores, bins=e, density=True)

            ax2.plot(c, ht, label="correctly pronounced")
            ax2.plot(c, hn, label="incorrectly pronounced")
            ax2.legend()

            fig.savefig("%s/plot_%s.pdf"%(output_dir, phone))
            plt.close()
        else:
            print("Not plotting phone %2s, due to too few samples, num_correct = %d, num_incorrect = %d"%(phone, len(neg_scores), len(pos_scores)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--data-for-eval-dir', dest='data_for_eval', help='Dir where data_for_eval.pickle is', default=None)
    parser.add_argument('--output-dir', dest='output_dir', help='Output dir', default=None)

    args = parser.parse_args()

    mkdirs(args.output_dir)
    scores = joblib.load(args.data_for_eval + 'data_for_eval.pickle')
    plots = plot(scores, args.output_dir)
