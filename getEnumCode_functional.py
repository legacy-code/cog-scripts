#!/usr/bin/python

import sys

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

    return lines


# -----================------

def myPrn(o):
    print o


# -----================------


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


# -----================------

def generateCodeForStringToEnum(funcName, arg, typeName, tupList):
    ''' generate the code '''

    genCode = GenEnumCode( typeName, arg, True )
    retStr = genCode.getFunctionHeaderStringToEnum(funcName)

    codeList = map( genCode.genEnumIfPart, tupList )
    retStr += reduce(lambda a, x: a + x, codeList, '' )

    retStr += genCode.getFunctionTailToEnum()
    return retStr


# -----================------



# -----================------


def generateCodeForEnumToString(funcName, arg, typeName, tupList):
    '''
    generate the code
    '''

    genCode = GenEnumCode( typeName, arg, False )
    retStr = genCode.getFunctionHeaderStringForEnum(funcName)

    codeList = map( genCode.genEnumCasePart, tupList )
    retStr += reduce(lambda a, x: a + x, codeList, '' )

    retStr += genCode.getFunctionTailForEnum()
    return retStr


# -----================------

class GenEnumCode( object ):

    def __init__( self, typename, arg, firsttime ):
        self.typeName = typename
        self.firstItem = firsttime
        self.arg = arg


    def getFunctionHeaderStringToEnum(self, funcName):
        headerString = """+ (%s)%s:(NSString *)%s
{
    """

        retStr = (headerString % (self.typeName, funcName, self.arg))
        return retStr

    def getFunctionTailToEnum(self):
        retStr = "}\n"
        return retStr



    def getFunctionHeaderStringForEnum(self, funcName):
        headerString = """+ (NSString *)%s:(%s)%s
{
    switch (%s)
    {
    """

        retStr = (headerString % (funcName, self.typeName, self.arg, self.arg))
        return retStr

    def getFunctionTailForEnum(self):
        retStr = """        default:
            return @"--";
    }
    """
        return retStr


    def genEnumCasePart( self, tup ):
        """
        case TDAIRAContributionCodeC1:
                return @"C1";
        """
        retStr = ""
        formatStr = '''case %s%s:
            return @"%s";
        '''

        retStr = (formatStr % ( self.typeName, tup[0], tup[0] ))

        return retStr

    def genEnumIfPart( self, tup ):
        """
        """
        retStr = ""
        formatStr = '''%sif ([%s isEqualToString:@"%s"])
        {
            return %s%s;
        }
        '''

        eClause = "else "
        if self.firstItem:
            eClause = ""
            self.firstItem = False

        retStr = (formatStr % (eClause, self.arg, tup[0], self.typeName, tup[0] ))

        return retStr


# -----================------




# --------------- main function - called from stand-alone --------------------------

def main( argv = None ):

    funcFromStringToEnum = "contributionCodeFromString"
    funcFromEnumToString = "stringFromContributionCode"

    lines = openAndReturnFile('test_input.txt')
    map(myPrn, lines)

    baseName = getEnumBaseName(lines)
    print "-- baseName -- ", baseName

    print "----- print tuples from obj-c enum -----"
    tups = getEnumTuples(lines)
    map(myPrn, tups)

    function1 = generateCodeForStringToEnum( funcFromStringToEnum, "code", baseName, tups )
    function2 = generateCodeForEnumToString( funcFromEnumToString, "code", baseName, tups )

    print "\n\n----- function1 -----\n", function1
    print "\n\n----- function2 -----\n", function2


# --------------- Run Script as stand-alone --------------------------

if __name__ == "__main__":
    sys.exit(main())

