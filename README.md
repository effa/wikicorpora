WikiCorpora
===========

WikiCorpora is a tool for building corpora from Wikipedia.

It's supposed to be run on Alba server in Natural Language Processing Centre
at the Faculty of Informatics, Masaryk University, Brno. Some portions of
the code can be run anywhere, but for full functionality WikiCorpora depends
on several NLP tools, such as unitok, desamb, treetagger and compilecorp.

Usage
-----

TBA (see `use-cases.txt`)

Environment configuration
-------------------------

Local environment configuration can be stored in `environment-config.yaml`.
As a fallback, `environment-config-default.yaml` is used. Content of these
configuration files is following:

```
paths:
    verticals:          '<path to directory for all verticals>'
    registry:           '<path to directory for registry files'
    compiled-corpora:   '<path to directory for compiled corpora>'
tools:
    unitok:             '<path to unitok>'
    sentence-tagger:    '<path to sentence-tagger script>'
    desamb:             '<path to desamb>'
    treetagger:         '<path to treetagger scripts (using substituable {lang})>'
    treetagger-en:      '<path to special treetagger script for english>'
```
