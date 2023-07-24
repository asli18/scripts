#!/bin/bash

# Function to extract and decompress all .tar.gz files in the given path
extract_tar_files() {
    local target_path="${1}"

    # Check if the specified path exists
    if [ -z "${target_path}" ]; then
        echo "Error: Please provide a target path."
        return 1
    fi

    if [ ! -d "${target_path}" ]; then
        echo "Error: The specified path does not exist."
        return 1
    fi

    # Find all files that match the condition in the specified path and process each found file
    find "${target_path}" -maxdepth 1 \
        -type f -name '*.tar.gz' -print0 \
    | while IFS= read -r -d '' f; do
        # Extract the base filename without the .tar.gz extension
        local filename=$(basename "${f}" .tar.gz)
        echo "${f} > ${filename}"
        tar xf "${f}" -C "${target_path}"
    done
}

# Call the function with the current directory as the target path
extract_tar_files "$(pwd)"
#extract_tar_files "."

