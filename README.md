# HTML Data Collector
Script to download the text from an HTTP response,
remove the boilerplate, and hash the original and resulting content to file.

## Requirements
* [Python 3.8+](https://www.python.org/)

All further requirements can be downloaded by using [Pipenv](https://pipenv.pypa.io/en/latest/):
`pipenv install` or through [pip](https://pip.pypa.io/en/stable/installation/):
`pip install -r requirements.txt`.

## Running Instructions
This program can be run using the following: `./main.py [URI]` where the URI
results in a valid HTTP response containing text.

This program can be run with many URIs from a file with [xargs](https://man7.org/linux/man-pages/man1/xargs.1.html):
`xargs -a [FILE] -I{} -d'\n' ./main.py {}`

For optional flags and more detail run `./main.py --help`.
