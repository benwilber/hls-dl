#!/usr/bin/env python3
#
#
import os
import m3u8
import requests
from argparse import ArgumentParser


CHUNK_SIZE = 10240


def fetch_segment(url, output_dir):
    print("\t", os.path.basename(url))
    r = requests.get(url, stream=True)
    r.raise_for_status()

    local_path = os.path.join(output_dir, os.path.basename(url))
    with open(local_path, 'wb') as f:
        for chunk in r.iter_content(CHUNK_SIZE):
            f.write(chunk)


def fetch_playlist(url, output_dir):
    print("Fetching", os.path.basename(url))
    r = requests.get(url)
    r.raise_for_status()

    local_path = os.path.join(output_dir, os.path.basename(url))
    with open(local_path, 'wb') as f:
        f.write(r.content)

    p = m3u8.load(url)
    if p.is_variant:
        for sp in p.playlists:
            fetch_playlist(sp.absolute_uri, output_dir)
    else:
        for s in p.segments:
            fetch_segment(s.absolute_uri, output_dir)


def main():
    parser = ArgumentParser(description="Download an HLS stream to a local directory.")
    parser.add_argument(
        '-o', '--output-dir', default=".",
        help="Local directory to save the stream.  Defaults to the current directory.")
    parser.add_argument('url', help="URL of the master HLS stream playlist to download.")
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    fetch_playlist(args.url, output_dir)


if __name__ == '__main__':
    main()
