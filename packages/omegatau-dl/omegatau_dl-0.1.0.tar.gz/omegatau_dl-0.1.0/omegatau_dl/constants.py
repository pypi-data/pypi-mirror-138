# Copyright (c) Marcel Johannfunke
# Licensed under the GPLv3 licence
# https://www.gnu.org/licenses/gpl-3.0.en.html

import re

NUMBER_RE_STR = "[0-9_]+"
NUMBER_RE = re.compile(NUMBER_RE_STR)
URL_ARCHIVE = "https://omegataupodcast.net/download-archive/"
URL_FEED = "https://omegataupodcast.net/feed/mp3/"
DL_RE = re.compile("[\"']https?://[^>]*?[(libsyn)(podlove)][^>]*?omegatau-?{NUMBER_RE_STR}[^>]*?\.mp3[\"']".format(NUMBER_RE_STR=NUMBER_RE_STR))
URL_EPISODE = "https://omegataupodcast.net/"

ARCHIVE_TITLE = {
    'en': "Older Episodes not in the Feed",
    'de': "Ältere Episoden die nicht im Feed sind",
    }

LANG_CATEGORY = {
    'en': "podcast (en)",
    'de': "podcast (de)",
}

DOWNLOAD_URL_CACHE_FILE = '.download_url_cache.json'

# This is just a band-aid for wrong episode urls
MANUAL_URLS = {
    # http://omegataupodcast.net/134-high-energy-neutrinos-and-the-icecube-neutrino-observatory/
    '135': '"http://traffic.libsyn.com/omegataupodcast/omegatau-135-highEnergyNeutrinosAndIceCube.mp3"',
    # Normal lookup for 150 leads to episode 150.5
    # http://omegataupodcast.net/150-the-european-extremely-large-telescope/
    '150': '"http://traffic.libsyn.com/omegataupodcast/omegatau-150-theEELT.mp3"',
    # http://omegataupodcast.net/150-5-controlling-the-elt/
    '150.5': '"http://traffic.libsyn.com/omegataupodcast/omegatau-150_5-eltControl.mp3"',
    # http://omegataupodcast.net/347-photosynthese/
    # Typo in filename
    '347': '"https://traffic.libsyn.com/secure/omegataupodcast/omegtau-347-photosynthese.mp3"',
    # https://omegataupodcast.net/363-eigenbau-pitts-model-12/
    # wrong number in filename
    '363': 'http://omegataupodcast.net/podlove/file/21/s/feed/c/mp3/omegatau-353-eigenbauPittsModel12.mp3',
}

MANUAL_LANG_URLS = {
    'en': {k: MANUAL_URLS[k] for k in MANUAL_URLS if k in [
        '135',
        '150',
        '150.5',
        ]},
    'de': {k: MANUAL_URLS[k] for k in MANUAL_URLS if k in [
        '347'
        ]},
}
