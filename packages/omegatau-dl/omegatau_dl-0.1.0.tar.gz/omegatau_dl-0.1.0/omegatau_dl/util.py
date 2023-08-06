# Copyright (c) Marcel Johannfunke
# Licensed under the GPLv3 licence
# https://www.gnu.org/licenses/gpl-3.0.en.html

from typing import (
    List, 
    Dict, 
    Tuple, 
    Union
    )
from .constants import *
import requests
import json
import os
import sys


def extract_number(url: str) -> Union[int, float]:
    start = url.rfind('/')
    # assumption: first number in link is the episode number
    m = NUMBER_RE.search(url[start if start >= 0 else 0:])
    if m is None:
        raise TypeError("No number found in url")
    number = m.group(0)
    if '_' in number:
        return float(number.replace('_', '.'))
    else:
        return int(m.group(0))


def number_idxs(url: str) -> Tuple[int, int]:
    m = NUMBER_RE.search(url)
    if m is None:
        raise TypeError("No number found in url")
    return m.span()


def scrape_missing_episodes(missing: List[int], lang: str = None) -> Dict[Union[int, float],str]:
    print("Trying to find downloads for missing episodes ...")
    missdict: Dict[Union[int, float], str] = {}
    known_urls: Dict[str, str] = {}
    if lang is None:
        try:
            # Load cached URLs to not have to scrape them again
            with open(DOWNLOAD_URL_CACHE_FILE, 'r') as f:
                known_urls.update(json.load(f))
        except FileNotFoundError:
            pass
    # put the saved cache file first and MANUAL_URLS later
    # so MANUAL_URLS can overwrite the file contents if neccessary
    known_urls.update(MANUAL_URLS if lang is None else MANUAL_LANG_URLS[lang])
    stillmissing: List[int] = []
    ignored: List[int] = []
    try:
        for number in missing:
            # Overwrite the existing line
            print("\rLooking for episode number {} ({}/{} missing episodes)".format(
                number, len(missdict)+len(ignored)+len(stillmissing)+1, len(missing)), end="")
            snumber = str(number)
            if snumber in known_urls:
                missdict[number] = known_urls[snumber]
                continue
            # Look for link in page
            pagetext = requests.get(URL_EPISODE+snumber).text
            dl_url_m = DL_RE.search(pagetext)
            # link not found
            if not dl_url_m:
                stillmissing.append(number)
                continue
            # if language filtering, then check language first
            if lang is not None:
                if LANG_CATEGORY[lang] not in pagetext:
                    ignored.append(number)
                    continue
            # link found, add to dict
            dl_url = dl_url_m.group(0)
            missdict[number] = dl_url

        print("\n")  # Prints empty line (above the same line was replaced)
        if stillmissing:
            print("Still missing episodes: {}".format(", ".join(map(str, stillmissing))))
            if missdict:
                print("Found download links for episodes: {}".format(", ".join(map(str, missdict.keys()))))
        else:
            print("Found download links for all episodes! =)")
    except KeyboardInterrupt:
        if lang is None:
            write_download_url_cache(missdict)
        raise KeyboardInterrupt()
    return missdict


def write_download_url_cache(missdict: Dict[Union[int, float], str]):
    # If the file cannot be written ignored
    # Cache is just meant to save some time on next usage
    try:
        with open(DOWNLOAD_URL_CACHE_FILE, 'w') as f:
            f.write(json.dumps(missdict, indent=4))
    except Exception as ignored:
        pass


def download_file(url: str, filename: str):
    nchunks = 0
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        print("Downloading {} ".format(filename), end='', flush=True)
        try:
            with open(filename, 'wb') as f:
                # 1 MiB chunks
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        nchunks += 1
                        # send . to show progress
                        if nchunks % 4 == 0:
                            print('.', end='', flush=True)
            print(" done")
        except KeyboardInterrupt:
            print("\nExiting...")
            os.remove(filename)
            print("Removed incomplete file")
            sys.exit(0)
