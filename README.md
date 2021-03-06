# pyexport

#### What is this?

A simple tool to log the exported functions from given DLLs.


File format:
```
DLL_PATH
OFFSET NAME ORDINAL
OFFSET NAME ORDINAL
OFFSET NAME ORDINAL
...
```
If two files are found with the same name, both of their exports will be written to the same output file. E.g.: `C:\test1.dll` and `C:\SomePath\test1.dll` will both be written to `OUTPUT_DIR/test1.dll.exports`, and the output will be (`test1.dll.exports`):

```
C:\test1.dll
OFFSET NAME ORDINAL
OFFSET NAME ORDINAL
OFFSET NAME ORDINAL
...
C:\SomePath\test1.dll
OFFSET NAME ORDINAL
OFFSET NAME ORDINAL
OFFSET NAME ORDINAL
...
```

#### Config format:
This tool uses yaml to store config information.

There are three types of configurations you can make:

* recurse_directories

    * Each entry is a full path to recursively search for DLLs

* flat_directories:

    * Each entry is a full path to search for DLLs non-recursively

* files:

    * Each entry is a single full path to a DLL


#### Usage:
```
usage: main.py [-h] -o OUTPUT_DIR [-c CONFIG]

Export parsing!

optional arguments:
  -h, --help     show this help message and exit
  -o OUTPUT_DIR  Directory where the export text files will be stored
  -c CONFIG      Use a provided yaml config file
  ```