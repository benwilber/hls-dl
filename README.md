# hls-dl
Download HLS video streams for local playback

## Installation

Install the dependencies in a virtualenv with:

```shell
$ pip install -r requirements.txt
```

## Usage
```shell
$ python3 hls-dl.py --help
usage: hls-dl.py [-h] [-o OUTPUT_DIR] [--start-pdt START_PDT] url

Download an HLS stream to a local directory.

positional arguments:
  url                   URL of the master HLS stream playlist to download.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Local directory to save the stream. Defaults to the current directory.
  --start-pdt START_PDT
                        Set the start Program Date Time in the HLS manifest.
```

## Examples

### Basic Usage
```shell
$ python3 hls-dl.py \
  --output-dir=my-stream \
  http://example.com/video/master.m3u8
```

### Set the #EXT-X-PROGRAM-DATE-TIME
```shell
$ python3 hls-dl.py \
  --start-pdt=2021-01-01T00:00:00Z \
  --output-dir=my-stream \
  http://example.com/video/master.m3u8
```

The HLS video stream will be downloaded to the directory `my-stream` and available for playback with [ffmpeg](https://ffmpeg.org/) via:

```shell
$ ffplay my-stream/master.m3u8
```
