import os
import sys
import glob
import pandas as pd

import ipdb

project_path = sys.argv[1]
dataset_dir = sys.argv[2]

list_of_labels = glob.glob(
    os.path.join(project_path, dataset_dir, '*', '*_labels.csv'))
list_of_predictions = glob.glob(
    os.path.join(project_path, dataset_dir, '*', '*_predictions.csv'))

for labels, predictions in zip(list_of_labels, list_of_predictions):
    df_labels = pd.read_csv(labels)
    df_predictions = pd.read_csv(predictions)

    acc = ((df_labels == df_predictions).sum() / df_labels.shape[0])[2:].mean()

    print('average accuracy for {} is {}%'.format(predictions, acc * 100))
