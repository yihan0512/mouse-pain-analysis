import os
import sys
import glob
import pandas as pd
from omegaconf import OmegaConf

from deepethogram import projects

import my_utils

if __name__ == '__main__':

    data_path = '/home/yi/Sunze/'
    project_name = 'mouse_pain_4'
    dataset_dir = sys.argv[2]
    label = sys.argv[3]

    behaviors = [
        'background', 'left_hindpaw_biting/licking',
        'right_hindpaw_biting/licking', 'genital_licking',
        'bout_of_hindpaw_scratchingandbiting'
    ]
    project_config = projects.initialize_project(
        data_path, project_name,
        behaviors)  # remember to change data destination
    project_config['project']['data_path'] = dataset_dir
    print(OmegaConf.to_yaml(project_config))

    new_movies_dir = sys.argv[1]
    list_of_movies = glob.glob(os.path.join(new_movies_dir, '*.avi'))
    mode = 'copy'  # or 'symlink' or 'move'
    # depending on the mode, it will copy, symlink, or move each video file
    # it will also compute the mean and standard deviation of each RGB channel
    # for movie_path in list_of_movies:
    #     projects.add_video_to_project(project_config, movie_path, mode=mode)

    # get paths of added movies
    search_string = os.path.join(project_name + '_deepethogram', dataset_dir,
                                 '*', '*.avi')
    print(search_string)
    list_of_new_movies = glob.glob(search_string)
    print(list_of_new_movies)

    if label == 'real':
        # add label files
        my_utils.prepare_labels(new_movies_dir, project_name + '_deepethogram',
                                dataset_dir)
    elif label == 'fake':
        # get label names
        df = pd.read_csv('./test.csv')
        cols = df.columns[1:]
        print(cols)

        # create fake label files
        for name in list_of_new_movies:
            my_utils.create_fake_labels(name, cols)
