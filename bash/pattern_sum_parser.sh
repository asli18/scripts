#!/bin/bash

check_input() {
    if [ $# -ne 3 ]; then
        echo "Error: Please input the pattern, field number, and target (directory or file path)"
        exit 1
    fi

    if [[ ! "$2" =~ ^[0-9]+$ ]]; then
        echo "Error: Field number is not a positive integer or zero"
        exit 1
    fi

    if [ ! -e "$3" ]; then
        echo "Error: The specified directory or file does not exist"
        exit 1
    fi
}

# Parser: Calculate the sum of values after matching the pattern in lines
parse_and_sum() {
    check_input "${@}"

    local pattern="${1}"
    local field_num="${2}"
    local target="${3}"
    local value=0

    if [ -d "${target}" ]; then
        # The path is a valid directory
        local file_ext=( -name '*.log' -o -name '*.txt' )  # valid file extensions as an array

        find "${target}" -maxdepth 1 -type f \( "${file_ext[@]}" \) -print0 \
        | while IFS= read -r -d '' f; do
            value=$(calculate_sum "${pattern}" "${field_num}" "${f}")
            echo "${f}:${pattern} ${value}"
        done

    elif [ -f "${target}" ]; then
        # The path is a valid file
        value=$(calculate_sum "${pattern}" "${field_num}" "${target}")
        echo "${value}"
    else
        echo "Error: The path is neither a valid directory nor a valid file"
        exit 1
    fi
}

# Calculate the sum of values in lines that match the pattern
calculate_sum() {
    local pattern="${1}"
    local field_num="${2}"
    local target="${3}"

    grep "${pattern}" "${target}" | \
        awk -v field="${field_num}" '{ sum += $field; } END { printf "%0.3f", sum }'
}

main() {
    parse_and_sum "${@}"
}

main "${@}"

