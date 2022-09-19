import os
import glob
from deepethogram import projects

project_path = '/home/yi/Sunze/mouse_pain_deepethogram'

projects.get_config_from_path(project_path)

sample_names = os.listdir(os.path.join(project_path, 'DATA'))

list_of_movies = glob.glob(os.path.join(project_path, 'DATA', '*_body', '*.avi'))
list_of_labels = glob.glob('/home/yi/Sunze/DATA/*.csv')

print(projects.)

print(list_of_movies)
print(list_of_labels)

# for movie_path, label_path in zip(list_of_movies, list_of_labels):
#     print(movie_path, label_path)
#     projects.add_label_to_project(label_path, movie_path)