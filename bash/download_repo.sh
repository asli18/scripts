#!/bin/bash

usage() {
    echo -e "Usage: ./download_repo.sh"
    echo -e "  -h, --help"
    echo -e "         display this help and exit\n"
    echo -e "  --update"
    echo -e "         Execute 'git pull' if the repo exists.\n"
    echo -e "  --depth=NUM"
    echo -e "         create a shallow clone of that depth\n"
    echo -e "  --lite"
    echo -e "         Clone the repo with the --single-branch option.\n"
    echo -e "Examples:"
    echo -e "  ./download_repo.sh                     # default"
    echo -e "  ./download_repo.sh --update            # download and update repo"
    echo -e "  ./download_repo.sh --depth=1           # set depth"
    echo -e "  ./download_repo.sh --depth=1 --lite --update"
}

main() {
    script_dir="$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 ; pwd -P)"
    cd ${script_dir}

    # Arguments
    local update=0
    local clone_depth=0
    local lite=0

    arg_parser "${@}"

    # clone repo_folder \
    #       branch \
    #       url

    clone sample_code \
          master \
          git@github.com:asli18/sample_code.git
}

arg_parser() {
    while [ "${1}" != "" ]; do
        PARAM=`echo ${1} | awk -F= '{print $1}'`
        VALUE=`echo ${1} | awk -F= '{print $2}'`
        case ${PARAM} in
            -h | --help)
                usage
                exit 0
                ;;
            --update)
                update=1
                ;;
            --depth)
                if ! is_int ${VALUE}; then
                    echo -e "Error: invalid depth value \"${VALUE}\""
                    usage
                    exit 1
                fi
                clone_depth=${VALUE}
                ;;
            --lite)
                lite=1
                ;;
            *)
                echo -e "Error: unknown parameter \"${PARAM}\""
                usage
                exit 1
                ;;
        esac
        shift
    done
}

is_int() {
    if [[ "${1}" =~ ^[0-9]+$ ]]; then
        return 0  # Return 0 to indicate it is an integer
    else
        return 1  # Return 1 to indicate it is not an integer
    fi
}

clone() {
    local repo_folder="$1"
    local branch="$2"
    local url="$3"

    local LYELLOW='\e[93m'
    local LGREEN='\e[92m'
    local NC='\e[0m'

    echo -e "--------------------------------"
    echo -e "Clone repo: ${LGREEN}${repo_folder}${NC}"
    echo -e "Branch:     ${LYELLOW}${branch}${NC}"

    if ! [ -d "${repo_folder}" ]; then
        local cmd="git clone"
        cmd+=" -b ${branch}"

        if [ "${lite}" -eq 1 ]; then
            echo -e "            ${LYELLOW}(single branch)${NC}"
            cmd+=" --single-branch"
        fi

        if [ "${clone_depth}" -ge 1 ]; then
            echo -e "Depth:      ${clone_depth}"
            cmd+=" --depth ${clone_depth}"
        fi

        cmd+=" ${url} ${repo_folder}"

        # git clone --depth ${clone_depth} -b ${branch} --single-branch ${url} ${repo_folder}
        ${cmd}

    elif [ "${update}" -eq 1 ]; then
        cd ${repo_folder}
        echo -e "Updating..."
        git pull
        cd - > /dev/null 2>&1
    else
        echo -e "Directory already exists."
    fi
}

main "${@}"


