import my_utils

import os
import pandas as pd


df = pd.read_csv('./mouse_pain_4_deepethogram/DATA/65_1_3wk_body/65_1_3wk_body_labels.csv')
cols = df.columns

video_path = './mouse_pain_4_deepethogram/DATA/65_1_3wk_body/65_1_3wk_body.avi'

my_utils.get_frame_count(video_path)

df = my_utils.create_fake_labels(video_path, cols)
print(df)

my_utils.clear_project_dirs('./mouse_pain_4_deepethogram/')

