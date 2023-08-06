# Copyright (c) Marcel Johannfunke
# Licensed under the GPLv3 licence
# https://www.gnu.org/licenses/gpl-3.0.en.html

import requests
import os.path
import argparse
from .constants import *
from .util import *
from . import version


def both(local_numbers):
    # Graceful exit on CTRL+C while looking for download links
    try:
        print("Downloading all (german and english) episodes")
        print("This script will ONLY download numbered episodes, you need to download special episodes manually.")
        print("Found {} episodes already downloaded.".format(len(local_numbers)))

        # Get text of archive webpage
        print("Getting episode list ...")
        pagetext_archive = requests.get(URL_ARCHIVE).text
        pagetext_feed = requests.get(URL_FEED).text

        # Parse all available download urls
        dl_urls: List[str] = DL_RE.findall(pagetext_archive) + DL_RE.findall(pagetext_feed)

        # put numbers on webpage in list
        numbers: List[Union[int, float]] = list(map(extract_number, dl_urls))
        maxnr = max(numbers)
        print("Found {} episodes in Archive, newest episode is {}".
              format(len(set(numbers)), maxnr))
        # List missing episodes
        all_numbers = list(range(1, maxnr+1))
        # Replace episode number 336 with 150.5 (was published as 150.5)
        all_numbers.append(150.5)
        all_numbers.remove(336)
        missing: List[int] = [x for x in all_numbers if x not in numbers]

        print("Missing episodes in Archive: {}".format(", ".join(map(str, missing))))

        # Check if some missing episodes are downloaded
        # then no need to find download link
        missing_but_downloaded = []
        for miss in missing:
            if miss in local_numbers:
                missing_but_downloaded.append(miss)

        if len(missing) == len(missing_but_downloaded):
            print("All missing episodes are already downloaded.")
        else:
            still_missing: List[int] = [miss for miss in missing
                             if miss not in missing_but_downloaded]

            if (missing_but_downloaded):
                print("Already downloaded missing episodes: {}".
                      format(", ".join(map(str, missing_but_downloaded))))
                print("Remaining episodes: {}".format(", ".join(map(str, still_missing))))

            missdict = scrape_missing_episodes(still_missing)
            for num, dl in missdict.items():
                numbers.append(num)
                dl_urls.append(dl)

    except KeyboardInterrupt:
        print("\nExiting ...")
        sys.exit(0)
    return dl_urls, numbers


def language(local_numbers, lang):
    # Graceful exit on CTRL+C while looking for download links
    try:
        print("Only downloading {} episodes".format(lang))
        print("This script will ONLY download numbered episodes, you need to download special episodes manually.")
        print("Found {} episodes already downloaded.".format(len(local_numbers)))

        # Get text of archive webpage
        print("Getting episode list ...")
        pagetext = requests.get(URL_ARCHIVE).text

        de_index = pagetext.index(ARCHIVE_TITLE['de'])
        en_index = pagetext.index(ARCHIVE_TITLE['en'])

        # Parse all available download urls
        dl_urls: List[str] = DL_RE.findall(pagetext)

        # put numbers on webpage in list
        numbers: List[Union[int, float]] = list(map(extract_number, dl_urls))
        maxnr = max(numbers)
        print("Found {} episodes in Archive, newest episode is {}".
              format(len(set(numbers)), maxnr))
        
        
        
        if lang == 'de':
            if de_index < en_index:
                pagetext = pagetext[de_index:en_index]
            else:
                pagetext = pagetext[de_index:]
        else:
            if en_index < de_index:
                pagetext = pagetext[en_index:de_index]
            else:
                pagetext = pagetext[en_index:]
        
        dl_urls: List[str] = DL_RE.findall(pagetext)
        numbers: List[Union[int, float]] = list(map(extract_number, dl_urls))
        max_lang_number = max(numbers)
        
        all_numbers = set(numbers)
        all_numbers.update(range(max_lang_number+1, maxnr+1))
        # Replace episode number 336 with 150.5 (was published as 150.5)
        if 336 in all_numbers:
            all_numbers.remove(336)
        all_numbers.add(150.5)
        # List missing episodes
        missing: List[int] = sorted([x for x in all_numbers if x not in numbers])
        
        print("Missing episodes in language specific Archive: {}".format(", ".join(map(str, missing))))

        # Check if some missing episodes are downloaded
        # then no need to find download link
        missing_but_downloaded = []
        for miss in missing:
            if miss in local_numbers:
                missing_but_downloaded.append(miss)

        if len(missing) == len(missing_but_downloaded):
            print("All missing episodes are already downloaded.")
        else:
            still_missing: List[int] = [miss for miss in missing
                             if miss not in missing_but_downloaded]

            if (missing_but_downloaded):
                print("Already downloaded missing episodes: {}".
                      format(", ".join(map(str, missing_but_downloaded))))
                print("Remaining episodes: {}".format(", ".join(map(str, still_missing))))

            missdict = scrape_missing_episodes(still_missing, lang=lang)
            for num, dl in missdict.items():
                numbers.append(num)
                dl_urls.append(dl)

    except KeyboardInterrupt:
        print("\nExiting ...")
        sys.exit(0)
    
    return dl_urls, numbers


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-de', '--ger', dest='lang', action='store_const', const='de', default=None)
    group.add_argument('-en', '--eng', dest='lang', action='store_const', const='en', default=None)
    group.add_argument('-dry', '--dry-mode', dest='dry', action='store_true', default=False)
    args = parser.parse_args()
    
    print("Checking version ...")
    if version.check():
        print("There is a new version available, consider updating with '{} -m pip install -U omegatau-dl'")
        answer = input("Continue with downloading episodes? [Y/n]")
        if answer.lower() in ['n', 'no']:
            return
    else:
        print("Version is up to date.")
    
    # numbers of episodes that are downloaded
    files: List[str] = [f for f in os.listdir(".") if f.startswith('omegatau') and f.endswith('.mp3')]
    local_numbers = set(map(extract_number, files))

    dl_urls, numbers = both(local_numbers) if args.lang is None else language(local_numbers, args.lang)

    print("\nStarting downloads ...\n")

    for dl_url, number in zip(dl_urls, numbers):
        # Already have it downloaded
        if number in local_numbers:
            continue
        # podlove has two numbers in string, need to do some special handling
        _filename = dl_url[dl_url.rindex('/')+1:]
        # Get number to put in 4 digit format
        start, end = number_idxs(_filename)
        # it seems XXr is a repaired episode?. strip the r
        after_number_char = _filename[end]
        endstr = _filename[end+1:-1] if after_number_char == 'r' else _filename[end:-1]
        # set local filename to 4 digit
        try:
            filename = "omegatau-" + "{:04d}".format(number) + endstr
        except ValueError:
            filename = "omegatau-" + "{:04.1f}".format(number).replace('.', '_') + endstr
        if not args.dry:
            download_file(dl_url[1:-1], filename)
        else:
            print(f"Download file: {dl_url} to {filename} (dry-run)")


if __name__ == "__main__":
    main()
 
