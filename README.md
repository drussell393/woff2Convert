This will convert woff2's from Google Fonts to TTF, and save it to an outfile on
most Unix-based systems (command-line) with Python.

# Quick Start Guide

This README cleanly documents how to use woff2Convert, but will not document how to
use, build, or run Google's woff2 compressor/decompressor. You should read their [README file](https://github.com/google/woff2/blob/master/README.md)
for more information about how to build woff2.

This assumes that you have **NOT** built woff2 yet, as there is a submodule that will
pull in the most recent version (from GitHub HTTPS) of woff2.

## Setup

There is minimal setup in starting with woff2Convert, but the following sections are good
to consider before attempting to use the script.

### Python Modules
You will need the following Python modules:

- PyYAML

You can get PyYAML using [pip](https://pip.pypa.io/en/stable/installing/). 

`pip install pyyaml`

We also use the following built-in Python modules:

- os
- sys
- getopt
- urllib2

We're going to assume you've made the python file executable:

`chmod +x woff2Convert.py`

### Configuration File

There is a YAML configuration file for default values. The values (mostly) can be
changed via the command line arguments, but I will list the description of each
configuration key here.

| Key              | Description                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| woff2Path        | The directory that your binaries for Google's woff2 exist[1].                                        |
| defaultOutputDir | The default directory to store the converted files in                                                |
| defaultFamily    | Not practical, but if you want to use a default font family when you don't specify it in the command |
| defaultCharset   | Google has many different charsets (eg. latin, vietnamese, latin-ext, etc).. default for that        |
| keepFile         | Do you wanna keep your woff2 files? If so, set this to "True" ... Boolean                            |


**[1]:** It is worth noting that this will likely be the woff2 directory inside the
woff2Convert directory if you used the submodule with this repo. You need to specify
the whole file path, though. It's **not** relative to the python file.

## Usage

The script accepts the following arguments:

| Argument                | Shorthand         | Description                       |
| ----------------------- | ----------------- | --------------------------------- |
| --family="Helvetica"    | -f "Helvetica"    | Font family you want to convert   |
| --outdir="/path/to/dir" | -o "/path/to/dir" | Path to the output directory      |
| --charset="latin"       | -c "latin"        | Character set that you want       |


All command arguments are optional, as you can technically define a default value for
all of them in the configuration file. However, it is unlikely that you will define a
value other than "None" for defaultFamily, so you will most likely use the command with
the `--family` value most.

Example usage:

`./woff2Convert.py --family="Noticia Text"`

Example shorthand usage:

`./woff2Convert.py -f "Noticia Text"`
