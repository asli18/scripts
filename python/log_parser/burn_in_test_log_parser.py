#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import re

from datetime import datetime


def timedelta_to_string(total_seconds):
    hours = int(total_seconds // 3600)
    remaining_seconds = total_seconds % 3600
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)

    formatted_output = f"{hours} hr {minutes} min {seconds} sec ({total_seconds} s)"
    return formatted_output


def get_datetime_format(s):
    datetime_format = ''
    for _ in range(2):
        if _ == 0:
            datetime_format = '[%a %b %d %H:%M:%S.%f %Y]'
        elif _ == 1:
            datetime_format = '[%Y-%m-%d %H:%M:%S.%f]'

        try:
            datetime.strptime(s, datetime_format)
            break
        except ValueError:
            datetime_format = ''
    return datetime_format


def calc_log_elapsed_time(file_name):
    err_pattern = re.compile(r'error|ERR|Error|Fail|FAIL|fail|wrong')

    last_valid_log_cnt = 5
    last_valid_log = []

    test_start_pattern = "calculating max progress..."
    datetime_format = ''
    dt_s = None
    dt_e = None
    loops = 0
    fail = False

    with open(file_name, 'r') as f:
        lines = f.readlines()

    for line in reversed(lines):
        if len(line[line.find(']')+1:].strip()) and len(last_valid_log) < last_valid_log_cnt:
            last_valid_log.append(line[line.find(']')+1:].strip())

        if line.startswith('[') and datetime_format == '':
            datetime_format = get_datetime_format(line[:line.find(']')+1])

            dt_e = datetime.strptime(line[:line.find(']')+1], datetime_format)

        if err_pattern.search(line) and not fail:
            fail = True

        if 'Burnin Loop=' in line and loops == 0:
            _ = line.split()[-1]
            loops = int(_[_.find('=')+1:])

        if test_start_pattern in line:
            dt_s = datetime.strptime(line[:line.find(']')+1], datetime_format)
            break

    if dt_s == None or dt_e == None or loops == 0:
        raise Exception('error: not burn-in log')

    print(f"start time:      {dt_s.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"end time:        {dt_e.strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\nResult: {'Fail' if fail else 'Pass'}")

    time_delta = dt_e - dt_s
    total_seconds = time_delta.total_seconds()

    print(f"Elapsed time: {timedelta_to_string(total_seconds)}")

    print(f"\nLoop = {loops}")
    if fail == False:
        print(f"Last valid log:")
        for line in reversed(last_valid_log):
            print(line)


def cleanup_and_exit(signal, frame):
    sys.exit(0)


def main():
    try:
        if len(sys.argv) < 2:
            print("arg not enough, enter file name: ", end="")
            file_name = input()
        else:
            file_name = sys.argv[1]

        calc_log_elapsed_time(file_name)
    except Exception as err:
        print(err)
    except:
        print(f"unexcepted error: {sys.exc_info()[0]}", file=sys.stderr)

    signal.signal(signal.SIGINT, cleanup_and_exit)
    print("Press Ctrl-C to exit...")
    while True:
        pass


if __name__ == '__main__':
    main()

