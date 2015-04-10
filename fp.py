
import sys

# __author__ = 'mike'



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

    return lines


def myPrn(o):
    print o

def getEnumBaseName( inIter ):
    '''
    assumming a line that looks something like this:
        typedef NS_ENUM(NSUInteger, TDAIRAContributionCode)
    we will return the TDAIRAContributionCode as the base
    :param inIter: iterable to look through
    :return: a string
    '''

    retStr = filter(lambda x: x.find('NS_ENUM') > -1, inIter)
    temp = retStr[0].split(',')
    retStr = temp[1].replace(")", "").strip()
    return retStr


# ---------- class for generating a tuple from Obj-c enum ---------
#    needed to allow a call from the map() function that has the
#    base name we need.  Trick from C++
#
class tupGenerator(object):
    def __init__(self, base ):
        self.baseName = base


    def tupFromLine(self, line ):
        if line.find(" = ") != -1:
            strName = ""
            idNum = ""
            comment = ""

        tupleList = line.split(" = ")
        strName = tupleList[0].replace(self.baseName, "").strip()
        if tupleList[1].find( "//" ) >= 0:
            tupleList = tupleList[1].split('//')
        else:
            tupleList = tupleList[1].split(',')
            if len(tupleList) >= 2:
                tupleList[1].replace('//', '')

        idNum = tupleList[0]
        if len(tupleList) >= 2:
            comment = tupleList[1]

        return (strName, idNum, comment)

# ---------- ----------

def getEnumTuples( inDict ):
    retList = list()

    baseName = getEnumBaseName( inDict )
    tg = tupGenerator( baseName )

    lines = filter(lambda x: x.find(' = ') > -1, inDict)
    retList = map( tg.tupFromLine, lines )
    return retList



# --------------- main function - called from stand-alone --------------------------

def main( argv = None ):

    lines = openAndReturnFile('test_input.txt')
    map(myPrn, lines)

    baseName = getEnumBaseName(lines)
    print "-- baseName -- ", baseName

    print "----- print tuples from obj-c enum -----"
    tups = getEnumTuples(lines)
    map(myPrn, tups)

# --------------- Run Script as stand-alone --------------------------

if __name__ == "__main__":
    sys.exit(main())

