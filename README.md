# m8_converter

Converts all `wav` files to 16-bit for use on the [Dirtywave M8](https://dirtywave.com/).

Copies all files in an input directory tree, converting `wav` files to 16-bit and skipping Ableton `asd` files. `m8_converter` will preserve your directory strucutre and is non-destructive. Additionally, it will skip a file if it already exists in the output directory (default `./output`). `m8_converter` uses Python's multiprocessing pool functionality to delegate file processing (evaluation, conversion, and/or copying) between all available processors, greatly speeding up the process of converting large amounts of files.

The program takes the following steps:

1. Walks through all files in the input directory
1. Determines the bit depth using `ffmpeg`
1. Converts the file if it
    1. is a `wav` file
    1. is not 16-bit
1. Otherwise, copies the file

Shoutout to [birds-inc](https://github.com/birds-inc/m8-sample-organizer) for giving me the idea to write this. Differences are the use of `ffmpeg-python`, multiprocessing, and not changing your directory structure/filenames. If you would like a way to perform this conversion and sort your files, then please check out their repo.

## Usage

Run `python m8_converter.py -h` for help output.

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

*This command will copy all files, converting those with a bit depth other than 16, to the directory `output`*

## Setup

### Prerequisites
1. Ensure you have `ffmpeg`
   - [Link to `ffmpeg` downloads](https://ffmpeg.org/download.html)
1. Ensure you have Python 3.12+
   - Required to use `pathlib`'s `walk()` method
1. Install requirements
   - `pip install -r requirements.txt`
   - This program uses the `ffmpeg-python` for Python bindings and `fortune-python` for fortunes in the help output
