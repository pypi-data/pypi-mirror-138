"""genmix

usage: genmix [-hvts] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database JSON file.
    -i MIXID, --mixid MIXID         Mixture IDs JSON file.
    -o OUTPUT, --output OUTPUT      Output HDF5 file.
    -t, --truth                     Save truth_t. [default: False].
    -s, --segsnr                    Save segsnr. [default: False].

Generate a SonusAI mixture file from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database JSON file.
    MIXID       A JSON file containing a list of mixture IDs. The list should be named 'mixid'.
                If no file is provided, then all mixtures in the database will be generated.

Outputs:
    OUTPUT.h5   A SonusAI mixture HDF5 file. Contains:
                    dataset:    mixture
                    dataset:    truth_t (optional)
                    dataset:    target
                    dataset:    noise
                    dataset:    segsnr (optional)
                    attribute:  mixdb
    genmix.log
"""
import json
from copy import deepcopy
from os.path import exists
from os.path import splitext
from typing import List
from typing import Union

import h5py
import numpy as np
from docopt import docopt
from pyaaware import ForwardTransform
from tqdm import tqdm

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import apply_augmentation
from sonusai.mixture import build_noise_audio_db
from sonusai.mixture import build_target_audio_db
from sonusai.mixture import generate_truth
from sonusai.mixture import get_mixtures_from_mixid
from sonusai.mixture import get_total_class_count
from sonusai.mixture import process_mixture_audio
from sonusai.utils import grouper
from sonusai.utils import human_readable_size
from sonusai.utils import int16_to_float
from sonusai.utils import seconds_to_hms
from sonusai.utils import trim_docstring


def genmix(mixdb: dict,
           mixid: Union[str, List[int]],
           compute_segsnr: bool = False,
           save_truth: bool = False,
           logging: bool = False,
           show_progress: bool = False,
           progress: tqdm = None) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict):
    mixdb_out = deepcopy(mixdb)
    mixdb_out['mixtures'] = get_mixtures_from_mixid(mixdb_out['mixtures'], mixid)

    if not mixdb_out['mixtures']:
        logger.error('Error processing mixid: {}; resulted in empty list of mixtures'.format(mixid))
        exit()

    total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])

    target = np.empty(total_samples, dtype=np.int16)
    noise = np.empty(total_samples, dtype=np.int16)
    truth_t = np.empty(0)
    if save_truth:
        truth_t = np.empty((mixdb_out['num_classes'], total_samples), dtype=np.single)

    segsnr = np.empty(0)
    fft = ForwardTransform(N=mixdb_out['frame_size'] * 4, R=mixdb_out['frame_size'])
    if compute_segsnr:
        segsnr = np.empty(total_samples, dtype=np.single)

    if logging:
        logger.info('')
        logger.info('Found {} mixtures to process'.format(len(mixdb_out['mixtures'])))
        logger.info('{} samples'.format(total_samples))

    noise_audios = build_noise_audio_db(mixdb_out)
    target_audios = build_target_audio_db(mixdb_out)

    i_sample_offset = 0
    i_frame_offset = 0
    o_frame_offset = 0
    if progress is None:
        progress = tqdm(total=len(mixdb_out['mixtures']), desc='genmix', disable=not show_progress)
    for mixture_record in mixdb_out['mixtures']:
        noise_audio, target_audio = process_mixture_audio(i_frame_offset=i_frame_offset,
                                                          i_sample_offset=i_sample_offset,
                                                          o_frame_offset=o_frame_offset,
                                                          mixdb=mixdb_out,
                                                          mixture_record=mixture_record,
                                                          target_audios=target_audios,
                                                          noise_audios=noise_audios)

        audio_indices = slice(i_sample_offset, i_sample_offset + len(target_audio))
        target[audio_indices] = target_audio
        noise[audio_indices] = noise_audio

        truth = generate_truth(mixdb=mixdb_out,
                               mixture_record=mixture_record,
                               target_audio=target_audio)
        if save_truth:
            truth_t[:, audio_indices] = truth

        if compute_segsnr:
            for offset in range(0, mixture_record['samples'], mixdb_out['frame_size']):
                target_energy = fft.energy(int16_to_float(target_audio[offset:offset + mixdb_out['frame_size']]))
                noise_energy = fft.energy(int16_to_float(noise_audio[offset:offset + mixdb_out['frame_size']]))
                frame_offset = i_sample_offset + offset
                segsnr[frame_offset:frame_offset + mixdb_out['frame_size']] = np.single(target_energy / noise_energy)

        i_sample_offset += mixture_record['samples']
        i_frame_offset += mixture_record['samples'] // mixdb_out['frame_size']
        o_frame_offset += mixture_record['samples'] // mixdb_out['feature_step_samples']
        progress.update()

    mixture = np.array(target + noise, dtype=np.int16)

    mixdb_out['class_count'] = get_total_class_count(mixdb_out)

    duration = len(mixture) / sonusai.mixture.sample_rate
    if logging:
        logger.info('')
        logger.info('Duration: {}'.format(seconds_to_hms(seconds=duration)))
        logger.info('mixture:  {}'.format(human_readable_size(mixture.nbytes, 1)))
        if save_truth:
            logger.info('truth_t:  {}'.format(human_readable_size(truth_t.nbytes, 1)))
        if compute_segsnr:
            logger.info('segsnr:   {}'.format(human_readable_size(segsnr.nbytes, 1)))

    return mixture, truth_t, target, noise, segsnr, mixdb_out


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        mixid_name = args['--mixid']
        output_name = args['--output']
        compute_segsnr = args['--segsnr']
        save_truth = args['--truth']

        if not output_name:
            output_name = splitext(mixdb_name)[0] + '.h5'

        log_name = 'genmix.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('genmix')

        if not exists(mixdb_name):
            logger.error('{} does not exist'.format(mixdb_name))
            exit()

        with open(mixdb_name, encoding='utf-8') as f:
            mixdb = json.load(f)

        if not mixid_name:
            mixid = list(range(len(mixdb['mixtures'])))
        else:
            if not exists(mixid_name):
                logger.error('{} does not exist'.format(mixid_name))
                exit()

            with open(mixid_name, encoding='utf-8') as f:
                mixid = json.load(f)
                if not isinstance(mixid, dict) or 'mixid' not in mixid.keys():
                    logger.error('Could not find ''mixid'' in {}'.format(mixid_name))
                    exit()
                mixid = mixid['mixid']

        mixdb_out = deepcopy(mixdb)
        mixdb_out['mixtures'] = get_mixtures_from_mixid(mixdb_out['mixtures'], mixid)

        if not mixdb_out['mixtures']:
            logger.error('Error processing mixid: {}; resulted in empty list of mixtures'.format(mixid))
            exit()

        total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])

        chunk_size = 50
        progress = tqdm(total=len(mixid), desc='genmix')
        mixid = grouper(range(len(mixdb_out['mixtures'])), chunk_size)
        mixdb_out['class_count'] = [0] * mixdb_out['num_classes']

        sample_offset = 0
        chunk_offset = 0
        truth_elems = 0
        with h5py.File(output_name, 'w') as f:
            for m in mixid:
                mixture, truth_t, target, noise, segsnr, mixdb_tmp = genmix(mixdb=mixdb_out,
                                                                            mixid=m,
                                                                            compute_segsnr=compute_segsnr,
                                                                            save_truth=save_truth,
                                                                            logging=False,
                                                                            progress=progress)

                samples = mixture.shape[0]
                if samples != truth_t.shape[1]:
                    logger.error(
                        'truth_t samples does not match mixture samples: {} != {}'.format(samples, truth_t.shape[1]))
                    exit()
                if samples != target.shape[0]:
                    logger.error(
                        'target samples does not match mixture samples: {} != {}'.format(samples, target.shape[0]))
                    exit()
                if samples != noise.shape[0]:
                    logger.error(
                        'noise samples does not match mixture samples: {} != {}'.format(samples, noise.shape[0]))
                    exit()
                if samples != segsnr.shape[0]:
                    logger.error(
                        'segsnr samples does not match mixture samples: {} != {}'.format(samples, segsnr.shape[0]))
                    exit()

                progress.refresh()
                if sample_offset == 0:
                    mixture_dataset = f.create_dataset(name='mixture',
                                                       data=mixture,
                                                       maxshape=(None,))
                    if save_truth:
                        truth_dataset = f.create_dataset(name='truth_t',
                                                         data=truth_t,
                                                         maxshape=(truth_t.shape[0], None))
                    target_dataset = f.create_dataset(name='target',
                                                      data=target,
                                                      maxshape=(None,))
                    noise_dataset = f.create_dataset(name='noise',
                                                     data=noise,
                                                     maxshape=(None,))
                    if compute_segsnr:
                        segsnr_dataset = f.create_dataset(name='segsnr',
                                                          data=segsnr,
                                                          maxshape=(None,))
                    truth_elems = truth_t.shape[0]
                else:
                    mixture_dataset.resize(sample_offset + samples, axis=0)
                    mixture_dataset[sample_offset:] = mixture
                    if save_truth:
                        truth_dataset.resize(sample_offset + samples, axis=1)
                        truth_dataset[:, sample_offset:] = truth_t
                    target_dataset.resize(sample_offset + samples, axis=0)
                    target_dataset[sample_offset:] = target
                    noise_dataset.resize(sample_offset + samples, axis=0)
                    noise_dataset[sample_offset:] = noise
                    if compute_segsnr:
                        segsnr_dataset.resize(sample_offset + samples, axis=0)
                        segsnr_dataset[sample_offset:] = segsnr
                sample_offset += samples

                for idx, val in enumerate(m):
                    mixdb_out['mixtures'][val] = mixdb_tmp['mixtures'][idx]
                for idx in range(mixdb_out['num_classes']):
                    mixdb_out['class_count'][idx] += mixdb_tmp['class_count'][idx]
                chunk_offset += chunk_size
            f.attrs['mixdb'] = json.dumps(mixdb_out)
        progress.close()

        logger.info('Wrote {}'.format(output_name))
        duration = total_samples / sonusai.mixture.sample_rate
        logger.info('')
        logger.info('Duration: {}'.format(seconds_to_hms(seconds=duration)))
        logger.info('mixture:  {}'.format(human_readable_size(sample_offset * 2, 1)))
        if save_truth:
            logger.info('truth_t:  {}'.format(human_readable_size(sample_offset * truth_elems * 4, 1)))
        logger.info('target:   {}'.format(human_readable_size(sample_offset * 2, 1)))
        logger.info('noise:    {}'.format(human_readable_size(sample_offset * 2, 1)))
        if compute_segsnr:
            logger.info('segsnr:   {}'.format(human_readable_size(sample_offset * 4, 1)))

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()


if __name__ == '__main__':
    main()
