#!/usr/bin/env python
# encoding: utf-8

"""Module for downloading huge files.
"""

from __future__ import unicode_literals
from contextlib import closing
from progressbar import ProgressBar
import hashlib
import urllib2

# download constants
CHUNK = 32 * 1024

# TODO nacitani osy (zobrazeni prubezneho vysledku stahovani)


def download_large_file(url, path, md5sum=None):
    """ Downloads large file from :url: to :path:

    :url: unicode
        url of file to download
    :path: unicode
        location where to download the file
    :md5sum: unicode [optional]
        md5 checksum
    """
    # download file and compute md5
    md5 = hashlib.md5()
    with closing(urllib2.urlopen(url)) as request:
        # read file size from headers
        file_size = int(request.info().getheaders('Content-Length')[0])
        print 'file size:', human_readable_size(file_size)
        downloaded = 0.0
        progressbar = ProgressBar()
        with open(path, 'wb') as output_file:
            while True:
                chunk = request.read(CHUNK)
                if not chunk:
                    break
                output_file.write(chunk)
                md5.update(chunk)
                downloaded += len(chunk)
                progressbar.update(downloaded / file_size)
        progressbar.finish()
    # check MD5 checksum
    if md5sum:
        if md5.hexdigest() == md5sum:
            print 'MD5 checksum: OK'
        else:
            print 'Wrong MD5 checksum! Try download the file again.'


def get_online_file(url, lines=False):
    """Retrieves online file and returns it as a string.

    :url: unicode
    :lines: if True, returns list of lines, else just one string

    :return: unicode || list of unicodes
    """
    with closing(urllib2.urlopen(url)) as request:
        if lines:
            return request.readlines()
        else:
            return request.read()


def human_readable_size(size):
    """Transforms byte size to human readable size with units

    :size: int
    :return: unicode
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return '{size:1.1f} {unit}'.format(size=size, unit=unit)
        size /= 1024.0
