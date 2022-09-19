from pymediainfo import MediaInfo
import pandas as pd
import numpy as np
import shutil
import os
import glob
import h5py

from omegaconf import DictConfig, OmegaConf
from deepethogram import projects
from deepethogram.postprocessing import get_postprocessor_from_cfg


def get_frame_count(video_path):
    media_info = MediaInfo.parse(video_path)
    n_frames = media_info.tracks[0].frame_count
    return int(n_frames)


def create_fake_labels(video_file_path, labels_name):
    n_frames = get_frame_count(video_file_path)
    arr = np.zeros((n_frames, len(labels_name)))
    df = pd.DataFrame(arr, columns=labels_name)

    save_path = os.path.join(
        os.path.dirname(video_file_path),
        os.path.splitext(os.path.basename(video_file_path))[0] + '_labels.csv')
    df.to_csv(save_path, index=True)


def prepare_labels(data_path, project_path, dataset_dir):
    """
    modify the format of existing label files
    """
    label_files = glob.glob(os.path.join(data_path, '*.csv'))

    for label_file in label_files:
        df = pd.read_csv(label_file)
        background = []
        for ind, row in df.iterrows():
            background.append(int(row.any()))
        df.insert(loc=0, column='background', value=background)

        df.to_csv(os.path.join(
            project_path, dataset_dir,
            os.path.splitext(os.path.basename(label_file))[0].strip('_Sunze'),
            os.path.basename(label_file).replace('Sunze', 'labels')),
                  index=True)


def clear_project_dirs(project_path):
    search_path = os.path.join(project_path, 'DATA', '*', '.ipynb_checkpoints')
    print(search_path)
    ignore = glob.glob(search_path)
    print(ignore)
    for name in ignore:
        print('removing {}...'.format(name))
        shutil.rmtree(name)

    search_path = os.path.join(project_path, 'DATA1', '*',
                               '.ipynb_checkpoints')
    print(search_path)
    ignore = glob.glob(search_path)
    print(ignore)
    for name in ignore:
        print('removing {}...'.format(name))
        shutil.rmtree(name)

    search_path = os.path.join(project_path, 'DATA', '.ipynb_checkpoints')
    print(search_path)
    ignore = glob.glob(search_path)
    print(ignore)
    for name in ignore:
        print('removing {}...'.format(name))
        shutil.rmtree(name)

    search_path = os.path.join(project_path, 'DATA1', '.ipynb_checkpoints')
    print(search_path)
    ignore = glob.glob(search_path)
    print(ignore)
    for name in ignore:
        print('removing {}...'.format(name))
        shutil.rmtree(name)


def postprocess_and_save(cfg: DictConfig) -> None:
    """Exports all predictions for the project
    Parameters
    ----------
    cfg : DictConfig
        a project configuration. Must have the `sequence` and `postprocessing` sections
        
    Goes through each "outputfile" in the project, loads the probabilities, postprocesses them, and saves to disk
    with the name `base + _predictions.csv`.
    """
    # the output name will be a group in the output hdf5 dataset containing probabilities, etc
    if cfg.sequence.output_name is None:
        output_name = cfg.sequence.arch
    else:
        output_name = cfg.sequence.output_name

    behavior_names = OmegaConf.to_container(cfg.project.class_names)
    records = projects.get_records_from_datadir(
        os.path.join(cfg.project.path, cfg.project.data_path))
    for _, record in records.items():
        with h5py.File(record['output'], 'r') as f:
            p = f[output_name]['P'][:]
            thresholds = f[output_name]['thresholds'][:]
            postprocessor = get_postprocessor_from_cfg(cfg, thresholds)

            predictions = postprocessor(p)
            df = pd.DataFrame(data=predictions, columns=behavior_names)
            base = os.path.splitext(record['rgb'])[0]
            filename = base + '_predictions.csv'
            df.to_csv(filename)
