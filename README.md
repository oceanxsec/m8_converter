# m8_converter

Converts all `wav` files to 16-bit for use on the [Dirtywave M8](https://dirtywave.com/).

The program takes the following steps:

1. Walks through all files in the input directory
1. Determines the bit depth using `ffmpeg`
1. Converts the file if it
    1. is a `wav` file
    1. is not 16-bit
1. Otherwise, copies the file

`m8_converter` will preserve your directory structure and will not interact with non-`wav` files, with the exception of skipping Ableton `asd` files.

## Usage

```
usage: m8_converter.py [-h] [--dry-run] [--output-directory OUTPUT_DIRECTORY] input_path                                                                                                    
Converts all samples to 16-bit wav

positional arguments:
  input_path            Input path for conversion

options:
  -h, --help            show this help message and exit
  --dry-run, -d         Does not make any changes
  --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        Set directory for processed files, default "./output"
```

### Example

`python m8_converter.py ./input`

*this command will copy all files, converting those with a bit depth other than 16, to the directory `output`*

## Setup

### Prerequisites
1. Ensure you have `ffmpeg`
   - [Link to `ffmpeg` downloads](https://ffmpeg.org/download.html)
1. Ensure you have Python 3.12+
   - Required to use `pathlib`'s `walk()` method
1. Install requirements
   - `pip install -r requirements.txt`