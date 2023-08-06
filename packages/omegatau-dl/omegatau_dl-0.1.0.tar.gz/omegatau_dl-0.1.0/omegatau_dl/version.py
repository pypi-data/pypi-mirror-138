# Copyright (c) Marcel Johannfunke
# Licensed under the GPLv3 licence
# https://www.gnu.org/licenses/gpl-3.0.en.html

import subprocess
import sys


__version__ = '0.1.0'


def check() -> bool:
    reqs = subprocess.run([sys.executable, '-m', 'pip', 'list','--outdated'], capture_output=True).stdout
    outdated_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return 'omegatau-dl' in outdated_packages

