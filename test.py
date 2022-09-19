import logging
import multiprocessing
import os
import random

import my_utils

# from google.colab import drive
import h5py
# not used in DeepEthogram; only to easily show plots
from IPython.display import Image
from omegaconf import OmegaConf
import pandas as pd
import torch

from deepethogram import configuration, projects, utils
from deepethogram.debug import print_dataset_info
from deepethogram.flow_generator.train import flow_generator_train
from deepethogram.flow_generator.inference import flow_generator_inference
from deepethogram.feature_extractor.train import feature_extractor_train
from deepethogram.feature_extractor.inference import feature_extractor_inference
from deepethogram.sequence.train import sequence_train
from deepethogram.sequence.inference import sequence_inference

if __name__ == '__main__':
    # prepare project
    project_path = '/home/yi/Sunze/mouse_pain_4_deepethogram'
    files = os.listdir(project_path)

    n_cpus = multiprocessing.cpu_count()
    print('n cpus: {}'.format(n_cpus))

    dataset_dir = 'DATA1'
    print_dataset_info(os.path.join(project_path, dataset_dir))

    my_utils.clear_project_dirs(project_path)

    # do feature extractor inference
    if 1:
        preset = 'deg_f'
        cfg = configuration.make_feature_extractor_inference_cfg(
            project_path=project_path, preset=preset)
        cfg.feature_extractor.weights = 'latest'
        cfg.flow_generator.weights = 'latest'
        cfg.inference.overwrite = True
        cfg.inference.ignore_error = False
        cfg.compute.num_workers = n_cpus
        print(OmegaConf.to_yaml(cfg))

        feature_extractor_inference(cfg)

    # do sequence inference
    if 1:
        cfg = configuration.make_sequence_inference_cfg(project_path)
        cfg.sequence.weights = 'latest'
        cfg.compute.num_workers = n_cpus
        cfg.inference.overwrite = True
        cfg.inference.ignore_error = False

        sequence_inference(cfg)

    # postprocssing
    if 1:
        cfg = configuration.make_postprocessing_cfg(project_path=project_path)
        my_utils.postprocess_and_save(cfg)
