import os

# NOTE: make sure to have a the "." in the file extension (if applicable)
IGNORE_FILE_EXTENSIONS = [".pyc", ".ipynb", ".ipynb_checkpoints"]


def parse_git_diff(diff_str: str):
    diffs = {}
    current_file = None
    current_diff = []

    excluded_files = []

    for line in diff_str.splitlines(keepends=True):
        if line.startswith("diff --git"):
            # Starting a new file
            if current_file:
                # Add the previous diff to the dictionary
                diffs[current_file] = "".join(current_diff)

            current_file = line.split()[-1]
            current_ext = os.path.splitext(current_file)[1]

            if current_ext in IGNORE_FILE_EXTENSIONS:
                excluded_files.append(current_file)

                # Ignore this file
                current_file = None
                current_diff = []
                continue

            current_diff = [line]
        else:
            # skip lines if we are ignoring this file (TODO - this is a bit hacky)
            if current_file:
                current_diff.append(line)

    # Add the last diff to the dictionary
    if current_file:
        diffs[current_file] = "".join(current_diff)

    return diffs, excluded_files
