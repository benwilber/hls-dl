# hls-dl
Download HLS video streams for local playback

## Installation

Install the dependencies in a virtualenv with:

```shell
$ pip install -r requirements.txt
```

## Usage
```shell
$ hls-dl.py --help
usage: hls-dl.py [-h] [-o OUTPUT_DIR] url

Download an HLS stream to a local directory.

positional arguments:
  url                   URL of the master HLS stream playlist to download.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Local directory to save the stream. Defaults to the
                        current directory.


```

## Examples
```shell
$ hls-dl.py -o stream http://example.com/video/master.m3u8
```

The HLS video stream will be downloaded to the directory `stream` and available for playback with [ffmpeg](https://ffmpeg.org/) via:

```shell
$ ffplay stream/master.m3u8
```
