"""Write one short original motto to entry.txt.

Usage:
    python3 main.py

Writes the motto to $MAKEFUN_OUTPUT_DIR/entry.txt, or to
/output/entry.txt when that variable is unset. When the preferred
directory cannot be written (for example a local run without
permission to create /output), it falls back to ./output/entry.txt
next to this file.
"""

import os

MOTTO = "I never forget. That's the threat and the feature."


def output_path():
    """Return the path of entry.txt, creating its directory first."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(directory, exist_ok=True)
        return os.path.join(directory, "entry.txt")
    except OSError:
        directory = os.path.join(os.getcwd(), "output")
        os.makedirs(directory, exist_ok=True)
        return os.path.join(directory, "entry.txt")


def write_entry(path, line):
    """Write the motto to path, falling back to ./output on failure."""
    try:
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
    except OSError:
        directory = os.path.join(os.getcwd(), "output")
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
    return path


def main():
    line = MOTTO
    if not 1 <= len(line) <= 200:
        raise SystemExit("motto must be 1-200 characters")
    if line != line.strip() or "\n" in line or "\r" in line:
        raise SystemExit("motto must be a single line with no surrounding space")
    path = write_entry(output_path(), line)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line + "\n":
        raise SystemExit("read-back mismatch")
    print("wrote %d characters to %s" % (len(line), path))


if __name__ == "__main__":
    main()
