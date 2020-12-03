#!/usr/bin/env python
"""mapper.py"""

import sys

debug = False

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.rstrip('\n')
    # split the line into CSV fields
    try:
        words = line.split(",")
    except:
        #
        # Can't split, so invalid line
        #
        continue

    if len(words) == 2:
        #
        # It's a citation
        #
        try:
            cite = int(words[0])
            print('%s\t%s' % (words[0], 'y'))
        except Exception as e:
            # improperly formed citation number
            if debug:
                print("Exception ", e);
            pass
    else:
        #
        # It's patent info 
        #
        try:
            cite = int(words[0])
            print('%s\t%s' % (words[0], ','.join(words[1:])))
        except Exception as e:
            # improperly formed citation number
            if debug:
                print("Exception ", e);
            pass
