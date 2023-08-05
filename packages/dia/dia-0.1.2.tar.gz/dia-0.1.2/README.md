Dia
===

Have you ever spent a long day at work, only to wonder at the end of it what you
actually got done? Do you wish you remembered why you made a decision way back when?
Do you want to find the day you worked on a specific thing, but haven't left any trace?

Dia solves all those problems by helping you keep a work diary.


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

This will generate the following `log.txt` in the current directory (or append to it if
it already exists):

```md
Work diary
==========


2022-02-09
----------

* Completed the diary feature.
```

# Changelog


## v0.1.2 (2022-02-09)

### Fixes

* Fix the help text for the "log" command. [Stavros Korokithakis]


## v0.1.1 (2022-02-09)

### Fixes

* Don't die if the diary file doesn't exist. [Stavros Korokithakis]


## v0.1.0 (2022-02-09)

### Fixes

* Fix program symlink. [Stavros Korokithakis]

* Fix program symlink. [Stavros Korokithakis]


