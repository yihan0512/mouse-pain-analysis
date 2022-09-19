import os
import sys
import glob
import pandas as pd

project_dir = sys.argv[1]
data_dir = os.path.join(project_dir, 'DATA')

samples = os.listdir(data_dir)

for sample in samples:
    if sample.endswith('_body'):
        print(sample)
        label_file = glob.glob(os.path.join(data_dir, sample, '*.csv'))[0]
        print(label_file)
        df = pd.read_csv(label_file)
        df = df.drop(df.columns[0], axis=1)
        df.to_csv(label_file, index=False)
