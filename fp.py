#!/usr/bin/env python

import sys

# __author__ = 'mike'



# -----================------

def openAndReturnFile( filename ):
    '''

    :param filename: file to open - if doesn't exist, will return empty list
    :return: lines of file (with \n|\r|',' stripped from the right)
    '''
    try:
        file = open(filename)
    except :
        print 'ERROR (openAndReturnFile(%s) - file not found!' % filename
        return list()

    lines = list()
    for line in file:
        lines.append(line.rstrip('\n').rstrip('\r').rstrip(','))

    file.close()
    return lines


# -----================------

def myPrn(o):
    print o





# --------------- main function - called from stand-alone --------------------------

def main( argv = None ):

    lines = openAndReturnFile('test_input.txt')
    map(myPrn, lines)


# --------------- Run Script as stand-alone --------------------------

if __name__ == "__main__":
    sys.exit(main())

