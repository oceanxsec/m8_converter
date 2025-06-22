from pathlib import Path
import argparse
import fortune
import ffmpeg
from multiprocessing import Pool
import sys
import shutil


# config options
target_codec = "pcm_s16le"
dry_run = None
output_directory = None


def main():
    parser = argparse.ArgumentParser(
        description="Converts all samples to 16-bit wav",
        epilog=fortune.fortune(),
    )
    parser.add_argument("input_path", help="Input path for conversion")
    parser.add_argument(
        "--dry-run", "-d", action="store_true", help="Does not make any changes"
    )
    parser.add_argument(
        "--output-directory",
        "-o",
        help='Set directory for processed files, default "./output"',
        default="output",
    )

    # parse input
    args = parser.parse_args()
    input_path = Path(args.input_path)
    global dry_run, output_directory
    dry_run = args.dry_run
    output_directory = args.output_directory

    # iterate through input path
    for dirpath, dirnames, filenames in input_path.walk():
        current_dir = Path(dirpath)
        print(f"Handling directory: {current_dir}")

        # iterate through each file, split work between processors
        with Pool() as pool:
            # get list of absolute paths for current directory
            absolute_paths = [current_dir.joinpath(filename) for filename in filenames]

            pool.map(handle_file, absolute_paths)

        if not dry_run:
            print(f"All files written to {output_directory}")


def handle_file(filepath: Path):
    # check if file is of type wav and what depth
    should_convert: bool = None
    reason: str = None
    skip_copy = False
    try:
        file_info = ffmpeg.probe(filepath)
        codec_name = file_info["streams"][0]["codec_name"]

        # determine if conversion is necessary
        if codec_name in target_codec:
            should_convert = False
            reason = f"Already encoded as {target_codec}"
        elif filepath.suffix != ".wav":
            should_convert = False
            reason = f"Only converting wav files, file is {filepath.suffix}"
        else:
            should_convert = True

    except ffmpeg.Error:
        should_convert = False
        reason = "Error reading"
    except IndexError:
        should_convert = False
        reason = "File did not contain streams"
    except KeyError:
        should_convert = False
        reason = "Key error"

    if "asd" in filepath.suffix:
        should_convert = False
        skip_copy = True
        reason = "Ableton .asd file"

    output_path = Path(output_directory) / filepath
    if not dry_run and not output_path.exists():

        # ensure path to file exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if should_convert:

            # handle conversion
            # model command:
            # ffmpeg -i input.wav -c:a pcm_s16le -ar 44100 output.wav
            try:

                # perform conversion
                input = ffmpeg.input(str(filepath))
                output_stream = ffmpeg.output(
                    input, str(output_path), acodec=target_codec, ar="44100"
                )
                ffmpeg.run(output_stream, overwrite_output=False, quiet=True)
                print(f"......Converted {filepath.name}")

            except ffmpeg.Error as e:

                # Catch and print any errors that ffmpeg-python might raise.
                print(f"......An error occurred during conversion: {e}")
                print(e.stderr.decode(), file=sys.stderr)

            except Exception as e:

                # Catch any other potential exceptions.
                print(f"......An unexpected error occurred: {e}")

        else:

            if not skip_copy:

                # copy from original directory to output directory
                # using copy2 to preserve metadata
                print(f"......Copying: {filepath.name}")
                shutil.copy2(filepath, output_path)
            else:
                print(f"......Skipping: {filepath.name} {reason}")

    elif output_path.exists():
        print("......File exists.")

    else:
        if not reason:
            reason = "Dry run"
        print(f"......Skipping: {filepath.name}, {reason}")


if __name__ == "__main__":
    main()
