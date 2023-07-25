# Automation and String Processing Scripts

This repository contains a collection of scripts showcasing automation and string processing techniques using various scripting languages.

## Bash scripts

- Demonstrates best practices for defining and using functions in Bash scripts.
    - [Download Git Repository](#download-git-repository)
    - [File Matching and Execution](#file-matching-and-execution)
    - [Log and Text File Parser](#log-and-text-file-parser)

---

## Download Git Repository

- Demonstrates various basic Bash usage scenarios, including:
    - Downloading a repository
    - Utilizing Bash functions
    - Parsing command-line arguments

### Usage

To use the `download_repo.sh` script, execute it as follows:
```bash
./download_repo.sh
```

---

## File Matching and Execution

Identify files with specified file extensions and perform operations on them.

### Usage

To use the `untar.sh` script, execute it as follows:
```bash
./untar.sh <directory>
    # <directory>: The path of the directory containing the .tar.gz files you want to extract.
./untar.sh /path/to/directory
```

---

## Log and Text File Parser

Parses log and text files, calculates the sum of values that match a specified pattern, and presents the results.

### Usage

To use the `pattern_sum_parser.sh` script, execute it with the following format:

```bash
./pattern_sum_parser.sh <pattern> <field_number> <target>
    # <pattern>:      The pattern to match in the file.
    # <field_number>: The field number whose values will be summed (a positive integer).
    # <target>:       The target directory or file path.

# Parse a single file and calculate the sum of matched values:
./pattern_sum_parser.sh "pattern" 3 /path/to/file.log
# Parse all log and text files in a directory and calculate the sum of matched values:
./pattern_sum_parser.sh "pattern" 2 /path/to/directory
```

---

## Perl
