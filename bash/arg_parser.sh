#!/bin/bash

usage() {
    echo -e "Usage: ./arg_parser.sh"
    echo -e "  -h, --help"
    echo -e "         display this help and exit\n"
    echo -e "  --update"
    echo -e "         Execute update\n"
    echo -e "  --num=NUM"
    echo -e "         NUM(Natural number)\n"
    echo -e "  -t, --target=TARGET"
    echo -e "         TARGET: ai, hpc\n"
    echo -e "Examples:"
    echo -e "  ./arg_parser.sh                     # default"
    echo -e "  ./arg_parser.sh --update            # enable update"
    echo -e "  ./arg_parser.sh --num=1             # set number"
    echo -e "  ./arg_parser.sh -t=ai,hpc           # select target"
    echo -e "  ./arg_parser.sh -t=ai --num=5 --update"
}

is_int() {
    if [[ "${1}" =~ ^[0-9]+$ ]]; then
        return 0  # Return 0 to indicate it is a positive integer or zero
    else
        return 1  # Return 1 to indicate it is not a positive integer or zero
    fi
}

arg_parser() {
    local PARAM
    local VALUE
    local target_param

    while [ "${1}" != "" ]; do
        PARAM=`echo ${1} | awk -F= '{print $1}'`
        VALUE=`echo ${1} | awk -F= '{print $2}'`
        case ${PARAM} in
            -h | --help)
                usage
                exit 0
                ;;
            -t | --target)
                target_param=${VALUE}
                ;;
            --update)
                update=1
                ;;
            --num)
                if ! is_int ${VALUE}; then
                    echo -e "Error: invalid number \"${VALUE}\""
                    usage
                    exit 1
                fi
                arg_num=${VALUE}
                ;;
            *)
                echo -e "Error: unknown parameter \"${PARAM}\""
                usage
                exit 1
                ;;
        esac
        shift
    done

    local targets="ai"
    [[ ! -z ${target_param} ]] && { targets=$(echo ${target_param} | tr "," " "); }

    for PARAM in ${targets}; do
        case ${PARAM} in
            ai)
                target_ai=1
                ;;
            hpc)
                target_hpc=1
                ;;
            *)
                echo -e "Error: unknown parameter \"${PARAM}\""
                usage
                exit 1
                ;;
        esac
    done
}

main() {
    local script_dir="$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 ; pwd -P)"
    cd ${script_dir}

    # Arguments
    local update=0
    local arg_num=0

    local target_ai=0
    local target_hpc=0

    arg_parser "${@}"

    echo -e "---- [ Arg List ] ----"
    echo -e "num:    ${arg_num}"
    echo -e "update: ${update}"
    echo -e "target: ai(${target_ai}), hpc(${target_hpc})"
}

main "${@}"

