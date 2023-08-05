Dia
===

Dia lets you keep a work log.


Installation
------------

Installing Dia is simple. You can use `pipx` (recommended):

```bash
$ pipx install dia
```

Or `pip` (less recommended):

```bash
$ pip install dia
```


Usage
-----

To log a task you've completed, you can use `dia log`:

```bash
$ dia log "Completed the diary feature."
```

This will generate the following `log.txt`:

```md
Work diary
==========


2022-02-09
----------

* Completed the diary feature.
```

# Changelog


## v0.1.1 (2022-02-09)

### Fixes

* Don't die if the diary file doesn't exist. [Stavros Korokithakis]


## v0.1.0 (2022-02-09)

### Fixes

* Fix program symlink. [Stavros Korokithakis]

* Fix program symlink. [Stavros Korokithakis]


