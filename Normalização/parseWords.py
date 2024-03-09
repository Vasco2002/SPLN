#!/usr/bin/env python3
import json
import pickle
import re

# python3 parseWords.py < words-top.txt > out.txt

def main():
    total =0
    data={}
    pattern = re.compile(r'(\w[\w\-]*\w|\w)\t(\d+).*')
    try:
        while True:
            line = input()
            match = pattern.match(line)
            if match:
                data[match.groups()[0]]=int(match.groups()[1])
    except EOFError:
        for k in data.keys():
            print(f"{k}")
            

if __name__ == "__main__":
    main()