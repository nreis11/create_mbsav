# Create mbsav

Creates a Mapping Buddy save file based on provided yaml file. 

## Getting Started

From project root, place desired yaml file in bin folder and run:

```
$ ./create_mbsav.sh <filename.yaml>
```
Output.mbsav will be created in bin folder if successful.

### Prerequisites

Python 2.7 or greater (Should run in Python 3 as well if you modify bash script)

## Known Issues
- Non-Roman characters will not be imported correctly in Mapping Buddy

## Authors

* **Nick Reis** - *Initial work*
