# exportTensorFlowLog
Export TensorFlow logs to common easy to read formats (csv-files, png-images, ...)
<table>
<tr>
<th>Summary</th>
<th>Format</th>
</tr>
<tr>
<td>Scalars</td>
<td>1 csv-file. One column per scalar summary tag.</td>
</tr>
<tr>
<td>Images</td>
<td>Multiple PNG-images structured in folders depending on the name of the summary tags.</td>
</tr>
<tr>
<td>Audio</td>
<td>Not yet supported.</td>
</tr>
<tr>
<td>Histograms</td>
<td>Not yet supported.</td>
</tr>
<tr>
<td>Distributions</td>
<td>Not yet supported.</td>
</tr>
<tr>
<td>Tensors</td>
<td>Not yet supported.</td>
</tr>
</table>

Tested on TensorFlow version 0.11.0, 1.1.0 and 1.3.0 and Python 2.7 and 3.6.

## Usage

```
usage: exportTensorFlowLog.py [-h]
                              [-s [{scalars,histograms,images,audio,compressedHistograms} [{scalars,histograms,images,audio,compressedHistograms} ...]]]
                              log out
Export tensorboard log file or directory of log files based on summary data.
positional arguments:
  log                   Location of log file or log directory containing logs.
  out                   Directory where log exports are stored.
optional arguments:
  -h, --help            show this help message and exit
  -s [{scalars,histograms,images,audio,compressedHistograms} [{scalars,histograms,images,audio,compressedHistograms} ...]]
                        The remaining arguments will be parsed as a list of
                        summaries. Default is to include all possible
                        summaries: [scalars, histograms, images, audio,
                        compressedHistograms].
```
