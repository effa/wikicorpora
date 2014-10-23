WikiCorpora
===========

WikiCorpora is a tool for building corpora from Wikipedia.

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
    compiled-corpora:   '<path to directory with compiled corpora>'
tools:
    unitok:             '<path to unitok>'
    desamb:             '<path to desamb>'
```
