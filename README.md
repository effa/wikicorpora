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
    registry:           '<path to directory for registry files'
    compiled-corpora:   '<path to directory for compiled corpora>'
tools:
    unitok:             '<path to unitok>'
    desamb:             '<path to desamb>'
    treetagger:         '<path to treetagger scripts (using substituable {lang})>'
    treetagger-en:      '<path to special treetagger script for english>'
```
