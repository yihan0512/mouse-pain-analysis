import sys
import pandas as pd

label_file = sys.argv[1]
label_file_1 = sys.argv[2]

df = pd.read_csv(label_file)
df1 = pd.read_csv(label_file_1)

# print('\n'.join(df.columns))
# print('\n'.join(df1.columns))

for i in range(-1, -19, -1):
    print('{} - {}'.format(df.columns[i], df1.columns[i]))