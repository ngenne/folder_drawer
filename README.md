# folderDrawer

This script allows you to obtain tree views of the directories browsed by one of the functions, as below:
![alt text](https://github.com/ngenne/folder_drawer/blob/main/img/example.png)


### Pre-requisites

This script calls upon on an open source project to work properly:

* https://github.com/njanakiev/folderstats - A great library to get some metadata about files and folders

__folderDrawer__ requires [Python](https://www.python.org/downloads/) 3.6+ to run.

First, make sure the dependencies are installed :
```sh
$ pip install -r requirements.txt
```

### Usage

Launch the script as below :
#### Unix
```sh
$ python folderDrawer.py "path/to/folder"
```
#### Windows
##### UNC path
```sh
C:\> python folderDrawer.py "\\path\to\folder"
```
OR
##### Local path
```sh
C:\> python folderDrawer.py "C:\path\to\folder"
```

It works from all CLI (Unix/Windows). Also, make sure to have permissions to read all contents through folders when you will use network paths, otherwise _folderstats_ will not be able to index the content.

### To Do

 - Find a solution for the first edge of the network which is reversed
