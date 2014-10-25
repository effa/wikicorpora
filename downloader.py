#!/usr/bin/env python
# encoding: utf-8

"""Module for downloading huge files.
"""

from contextlib import closing
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
        with open(path, 'wb') as output_file:
            while True:
                chunk = request.read(CHUNK)
                if not chunk:
                    break
                output_file.write(chunk)
                md5.update(chunk)

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
