# scan2map

This script allows you to obtain tree views of the directories browsed by one of the functions.


### Pre-requisites

This script calls upon on an open source project to work properly:

* https://github.com/njanakiev/folderstats - A great library to get some metadata about files and folders


### Usage

__scan2map__ requires [Python](https://www.python.org/downloads/) 3.6+ to run.

First, make sure the dependencies are installed :
```sh
$ pip install networkx pandas folderstats
```
Second, launch the script as below :
```sh
$ python scan2map.py "path/to/folder"
```

It works from all CLI (Unix/Windows). On Windows, you might encounter some problems about very long path to files/folders (> 256 characters). Also, make sure to have permissions to read all contents through folders when you will use network paths, otherwise _folderstats_ will not be able to index the content.

### To Do

 - Find a solution for the first edge of the network which is reversed

License
----

MIT

