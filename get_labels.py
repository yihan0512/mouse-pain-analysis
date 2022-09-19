import sys
import pandas as pd

label_file = sys.argv[1]

df = pd.read_csv(label_file)

print(len(df.columns))
print('\n'.join(df.columns))

with open('labels.txt', 'w+') as f:
    f.write("',\n'".join(df.columns))