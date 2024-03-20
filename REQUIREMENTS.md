# slogpy Design Document

[[_TOC_]]

## Intent
The intentions is to have a module that is simple to use and covers the majority of the logging needs for Python scripts and modules across the various target areas including (but not necessarily limited to):

* Casual and Production scripts running on local (dev) machines.
* Scripts/modules used in ADO pipelines (build logging)


## Requirements

1. Ability to log to console only
1. Ability to log to console and file
1. Automatic log file selection with ability to override and choose a specific path/filename
1. Automatic start fencepost in log file upon initialization of logging
1. Ability to write end fencepost in log file (conclusion of script)
1. Header functionality
1. Depth selection
1. Operation Start/Elapsed/Ended
1. Progress bar
1. Log from multiple concurrent scripts

## Design

### Headers
```python
log.header('Download Manifests')
log.header('merge-manifest', minor=True)
```

```text
==================
Download Manifests
==================
--------------------
merge-manifest
--------------------
```

### Depth Selection
```python
log.info('Download Manifests')
log.info('merge-manifest', depth=1)
log.info('downloading', depth=2)
log.info('complete', depth=2)
```

```text
Downloading Manifests
-- merge-manifest
---- downloading
---- complete
```

### Operation Start/Elapsed/End
```python
```

```text
```

There are different ways of doing this, sort of thinking 
```python
```