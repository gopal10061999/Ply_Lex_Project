#!/usr/bin/env python
"""combiner.py"""

import sys

def combine_input():
    """Combine input lines."""
    for line in sys.stdin:
        line = line.strip().replace("::", ":0:").replace("N/A", "0")
        print(line)

if __name__ == "__main__":
    combine_input()
