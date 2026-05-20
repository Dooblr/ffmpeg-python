#!/usr/bin/env python3
import subprocess
import sys
import os

SUPPORTED_FORMATS = ["mp3", "wav", "flac", "aac", "ogg", "m4a", "opus", "wma", "aiff"]


def check_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is not installed or not found in PATH.")
        sys.exit(1)


def get_input_path():
    while True:
        path = input("Enter the path to the audio file: ").strip().strip("'\"")
        if not path:
            print("  Path cannot be empty. Please try again.")
            continue
        if not os.path.isfile(path):
            print(f"  File not found: {path!r}. Please try again.")
            continue
        return path


def get_output_format():
    print(f"\nSupported formats: {', '.join(SUPPORTED_FORMATS)}")
    while True:
        fmt = input("Enter the output file format (e.g. mp3): ").strip().lower().lstrip(".")
        if not fmt:
            print("  Format cannot be empty. Please try again.")
            continue
        if fmt not in SUPPORTED_FORMATS:
            print(f"  Unsupported format '{fmt}'. Choose from: {', '.join(SUPPORTED_FORMATS)}")
            continue
        return fmt


def build_output_path(input_path: str, output_format: str) -> str:
    base, _ = os.path.splitext(input_path)
    output_path = f"{base}.{output_format}"

    # Avoid overwriting the source file
    if os.path.abspath(output_path) == os.path.abspath(input_path):
        output_path = f"{base}_converted.{output_format}"

    return output_path


def convert(input_path: str, output_path: str):
    print(f"\nConverting: {input_path}")
    print(f"        to: {output_path}\n")

    cmd = ["ffmpeg", "-y", "-i", input_path, output_path]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Conversion failed. ffmpeg output:")
        print(result.stderr)
        sys.exit(1)

    size = os.path.getsize(output_path)
    print(f"Done! Output file: {output_path}  ({size / 1024:.1f} KB)")


def main():
    check_ffmpeg()

    input_path = get_input_path()
    output_format = get_output_format()
    output_path = build_output_path(input_path, output_format)

    convert(input_path, output_path)


if __name__ == "__main__":
    main()
