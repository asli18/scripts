#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("--- [ read ] ---")
with open('data.txt', 'r') as f:
    data=f.read()
print(data)
print(f"len(data)    = {len(data)}")
print(f"len(data[0]) = {len(data[0])}")
print(f"len(data[1]) = {len(data[1])}")
print()

print("--- [ readlines ] ---")
with open('data.txt', 'r') as f:
    lines=f.readlines()

print(data)
print(f"len(lines)    = {len(lines)}")
print(f"len(lines[0]) = {len(lines[0])}")
print(f"len(lines[1]) = {len(lines[1])}")

for line_number, line in enumerate(lines, start=1):
    index = line.find('xyz')
    if index != -1:
        print(f"Found 'xyz' in line {line_number}, position {index + 1}: {line.strip()}")

