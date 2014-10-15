#!/usr/bin/env python
# encoding: utf-8

from system_utils import choose_path
import bz2
from lxml import etree

# TODO: logovani misto printu, vyzkouseni jinych zpusobu parsovani xml


def create_sample_dump(lang=None, size=10, dump_path=None, sample_path=None):
    """ Creates smaller sample dump from large dump of given language

    :lang: alpha-2 code of language of the dump
    """
    # check if either language or dump path is specified
    if not lang and not dump_path:
        raise ValueError('Either language or dump_path has to be specified')

    # select input and output file names
    dump_path = dump_path or choose_path(lang, 'xml.bz2', description='dump')
    sample_path = sample_path or choose_path(lang, 'xml',
        description='dump-sample-size-' + str(size))

    # check if the input file is xml or bzipped xml
    if not dump_path.endswith('.xml') and not dump_path.endswith('.xml.bz2'):
        raise ValueError('Dump file has to be xml or bzipped xmml.')

    # use bz2 library to read bzipped file
    bzipped = dump_path.endswith('.bz2')
    dump_file = bz2.BZ2File(dump_path, 'r') if bzipped else dump_path

    # find the namespace: read first event, which is ('start', root element),
    # and then get namespace information from the root element
    context_for_ns = etree.iterparse(dump_file, events=('start',))
    _, root = context_for_ns.next()
    # None znamena impliciti namesapce (without prefix)
    namespace = root.nsmap[None]
    del context_for_ns
    # reopen bzipped file
    if bzipped:
        dump_file = bz2.BZ2File(dump_path, 'r')

    # iterate through xml and build a sample file
    page_tag = '{{{namespace}}}page'.format(namespace=namespace)
    context = etree.iterparse(dump_file, events=('end',), tag=page_tag)
    #context = etree.iterparse(dump_file, events=('end',), tag="{*}page")
    sample_root = etree.Element('mediawiki', nsmap={None: namespace})
    pages = 0
    for event, elem in context:
        sample_root.append(elem)
        pages += 1
        if pages == size:
            break

    # write sample xml to file
    with open(sample_path, 'w') as sample_file:
        sample_file.write(etree.tostring(sample_root, pretty_print=True))

    # log info (TODO: logging)
    print 'Sample of {pages} pages created at {path}'.format(
          pages=pages, path=sample_path)
