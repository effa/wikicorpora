#!/usr/bin/env python
# encoding: utf-8

"""Module for downloading wiki dumps.
"""

from contextlib import closing
from system_utils import choose_path
#import logging
#import sys
import urllib2

# download constants
DUMP_URL_GENERAL = 'http://dumps.wikimedia.org/{lang}wiki/latest/' \
    + '{lang}wiki-latest-pages-articles.xml.bz2'
CHUNK = 32 * 1024

# logging setting
# TODO udelat logovani poradne
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#logging_handler = logging.StreamHandler(sys.stdout)
#formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
#logging_handler.setFormatter(formatter)
#logger.addHandler(logging_handler)


def download_dump(lang, path=None):
    """ Downloads wikipedia dump for given language
    """
    # initialization: select dump path and url
    dump_url = DUMP_URL_GENERAL.format(lang=lang)
    path = path or choose_path(lang, 'xml.bz2', description='dump')

    #logger.info('Start downloading {lang}-wiki dump from {url} into {path}'.
    #            format(lang=lang, url=dump_url, path=path))
    print 'Start downloading {lang}-wiki dump from {url} into {path}'\
          .format(lang=lang, url=dump_url, path=path)

    # downloading
    with closing(urllib2.urlopen(dump_url)) as request:
        with open(path, 'wb') as dump_file:
            pass
            while True:
                chunk = request.read(CHUNK)
                if not chunk:
                    break
                dump_file.write(chunk)

    # TODO check MD5 checksums

    #logger.info('Downloading finished: {lang}-wiki dump is in {path}'.format(
    #    lang=lang,
    #    path=path))
    print 'Downloading finished: {lang}-wiki dump is in {path}'.format(
        lang=lang,
        path=path)
