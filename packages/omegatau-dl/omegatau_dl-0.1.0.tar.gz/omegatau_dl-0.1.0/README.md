# Requirements

`Python 3` and `pip` for Python 3.

# Usage

Use `pip` to install this package
```
pip install omegatau-dl
pip3 install omegatau-dl
```
depending on your OS and Python version supported by `pip`.
On most Linux distributions `python`/`pip` refers to Python 2 and `python3`/`pip3` to Python 3.

Then run the script with
```
python -m omegatau_dl
python3 -m omegatau_dl
```
depending on your OS.

The script will download all numbered episodes into the same folder.
It won't redownload existing episodes.
It **does not** support continuation of download, so if you stop in the middle of a download delete that (incomplete) file. 
The numbers of all downloaded episodes will all be converted to 4 digit numbers.

With the options `-de` or `-en` the script will only download th episodes of the respective language.
