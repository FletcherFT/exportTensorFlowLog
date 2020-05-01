import time
import csv
import collections
import argparse
from pathlib import Path

# Import the event accumulator from Tensorboard. Location varies between Tensorflow versions. Try each known location
# until one works.
eventAccumulatorImported = False
# TF version < 1.1.0
if not eventAccumulatorImported:
    try:
        from tensorflow.python.summary import event_accumulator

        eventAccumulatorImported = True
    except ImportError:
        eventAccumulatorImported = False
# TF version = 1.1.0
if not eventAccumulatorImported:
    try:
        from tensorflow.tensorboard.backend.event_processing import event_accumulator

        eventAccumulatorImported = True
    except ImportError:
        eventAccumulatorImported = False
# TF version >= 1.3.0
if not eventAccumulatorImported:
    try:
        from tensorboard.backend.event_processing import event_accumulator

        eventAccumulatorImported = True
    except ImportError:
        eventAccumulatorImported = False
# TF version = Unknown
if not eventAccumulatorImported:
    raise ImportError('Could not locate and import Tensorflow event accumulator.')

summariesDefault = ['scalars', 'histograms', 'images', 'audio', 'compressedHistograms']


class Timer(object):
    # Source: https://stackoverflow.com/a/5849861
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name)
            print('Elapsed: %s' % (time.time() - self.tstart))


parser = argparse.ArgumentParser(description="Export tensorboard log file or directory of log files based on summary"
                                             " data.")
parser.add_argument("log", type=str, help="Location of log file or log directory containing logs.")
parser.add_argument("out", type=str, help="Directory where log exports are stored.")
parser.add_argument("-s", nargs="*", choices=summariesDefault, help="The remaining arguments will be parsed as a list "
                                                                    "of summaries. Default is to include all possible "
                                                                    "summaries: [scalars, histograms, images, audio, "
                                                                    "compressedHistograms].", default=summariesDefault)
args = parser.parse_args()

log = Path(args.log).resolve()

logs = [str(log)]

if log.is_dir():
    logs = log.rglob("events.out.tfevents.*")

output_dir = Path(args.out).resolve()

for run in logs:
    output_path = output_dir.joinpath(run.parent.name)
    output_path.mkdir(parents=True, exist_ok=True)

    with Timer():
        ea = event_accumulator.EventAccumulator(str(run),
                                                size_guidance={
                                                    event_accumulator.COMPRESSED_HISTOGRAMS: 0,  # 0 = grab all
                                                    event_accumulator.IMAGES: 0,
                                                    event_accumulator.AUDIO: 0,
                                                    event_accumulator.SCALARS: 0,
                                                    event_accumulator.HISTOGRAMS: 0,
                                                })

    with Timer():
        ea.Reload()

    tags = ea.Tags()
    for t in tags:
        tagSum = []
        if isinstance(tags[t], collections.Sequence):
            tagSum = str(len(tags[t])) + ' summaries'
        else:
            tagSum = str(tags[t])
        print('   ' + t + ': ' + tagSum)

    if 'audio' in args.s:
        print(' ')
        print('Exporting audio...')
        with Timer():
            print('   Audio is not yet supported!')

    if 'compressedHistograms' in args.s:
        print(' ')
        print('Exporting compressedHistograms...')
        with Timer():
            print('   Compressed histograms are not yet supported!')

    if 'histograms' in args.s:
        print(' ')
        print('Exporting histograms...')
        with Timer():
            print('   Histograms are not yet supported!')

    if 'images' in args.s:
        print(' ')
        print('Exporting images...')
        imageDir = output_path.joinpath('images')
        imageDir.mkdir(parents=True, exist_ok=True)
        print('Image dir: {}'.format(imageDir))
        with Timer():
            imageTags = tags['images']
            for imageTag in imageTags:
                images = ea.Images(imageTag)
                imageTagDir = imageDir.joinpath(imageTag)
                imageTagDir.mkdir(parents=True, exist_ok=True)
                for image in images:
                    imageFilename = imageTagDir.join("{}.png".format(image.step))
                    with open(imageFilename, 'wb') as f:
                        f.write(image.encoded_image_string)

    if 'scalars' in args.s:
        print(' ')
        csvFileName = output_path.joinpath("scalars.csv")
        print('Exporting scalars to csv-file...')
        print('   CSV-path: {}'.format(csvFileName))
        scalarTags = tags['scalars']
        with Timer():
            with open(csvFileName, 'w', newline='') as csvfile:
                logWriter = csv.writer(csvfile, delimiter=',')

                # Write headers to columns
                headers = ['wall_time', 'step']
                for s in scalarTags:
                    headers.append(s)
                logWriter.writerow(headers)

                vals = ea.Scalars(scalarTags[0])
                for i in range(len(vals)):
                    v = vals[i]
                    data = [v.wall_time, v.step]
                    for s in scalarTags:
                        scalarTag = ea.Scalars(s)
                        S = scalarTag[i]
                        data.append(S.value)
                    logWriter.writerow(data)
