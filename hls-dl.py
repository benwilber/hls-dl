#!/usr/bin/env python3
#
#
import os
import m3u8
import requests
from argparse import ArgumentParser
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse as parse_datetime


CHUNK_SIZE = 10240


def fetch_segment(url, output_dir):
    """ Fetch a single MPEG-TS segment to `output_dir`.
    """
    print("\t", os.path.basename(url))
    r = requests.get(url, stream=True)
    r.raise_for_status()

    local_path = os.path.join(output_dir, os.path.basename(url))
    with open(local_path, 'wb') as f:
        for chunk in r.iter_content(CHUNK_SIZE):
            f.write(chunk)


def fetch_playlist(url, output_dir, start_pdt=None):
    """ Fetch an M3U8 playlist recursively and store the full
        contents in `output_dir`.
    """
    print("Fetching", os.path.basename(url))

    p = m3u8.load(url)

    m = m3u8.M3U8()
    m.version = p.version
    m.target_duration = p.target_duration
    m.media_sequence = p.media_sequence

    if p.is_variant:
        for sp in p.playlists:
            fetch_playlist(sp.absolute_uri, output_dir, start_pdt=start_pdt)
    else:
        current_pdt = start_pdt
        for s in p.segments:
            if current_pdt:
                s.program_date_time = current_pdt
                current_pdt = current_pdt + timedelta(seconds=s.duration)

            # fetch_segment(s.absolute_uri, output_dir)
            m.add_segment(s)

    local_path = os.path.join(output_dir, os.path.basename(url))
    with open(local_path, 'w') as f:
        f.write(m.dumps())



def main():
    parser = ArgumentParser(description="Download an HLS stream to a local directory.")
    parser.add_argument(
        '-o', '--output-dir', default=".",
        help="Local directory to save the stream.  Defaults to the current directory.")
    parser.add_argument(
        "--start-pdt",
        type=parse_datetime,
        help="Set the start Program Date Time in the HLS manifest."
    )
    parser.add_argument('url', help="URL of the master HLS stream playlist to download.")
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    fetch_playlist(args.url, output_dir, start_pdt=args.start_pdt)


if __name__ == '__main__':
    main()
