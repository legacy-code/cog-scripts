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

    file.close()
    return lines


# -----================------

def myPrn(o):
    print o


# -----================------


# ---------- class for generating a tuple from Obj-c enum ---------
#    needed to allow a call from the map() function that has the
#    base name we need.  Trick from C++
#
class tupGenerator(object):

    # ----------
    def __init__(self, filename ):
        ''' read in the file and do the appropriate thingss '''
        self.lines = openAndReturnFile('test_input.txt')
        #map(myPrn, self.lines)
        self.baseName = self.getEnumBaseName()

    # ----------
    def tupFromLine(self, line ):
        '''
        line will look something like this:
                TDAIRAContributionCodeC2 = 2,   // IRA Contribution Previous Year
        will want to get each part -- assumes that have an ' = ' or it won't parse
        '''
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

    # ----------
    def getEnumTuples( self ):
        retList = list()

        lines = filter(lambda x: x.find(' = ') > -1, self.lines)
        retList = map( self.tupFromLine, lines )
        return retList

    # ----------
    def getEnumBaseName( self ):
        '''
        assumming a line that looks something like this:
            typedef NS_ENUM(NSUInteger, TDAIRAContributionCode)
        we will return the TDAIRAContributionCode as the base
        :param inIter: iterable to look through
        :return: a string
        '''
        retStr = filter(lambda x: x.find('NS_ENUM') > -1, self.lines)
        temp = retStr[0].split(',')
        retStr = temp[1].replace(")", "").strip()
        return retStr




# -----================------

class GenEnumCode( object ):

    # ----------
    def __init__( self, typename, arg, firsttime ):
        self.typeName = typename
        self.firstItem = firsttime
        self.arg = arg


    # ----------
    def getFunctionHeaderStringToEnum(self, funcName):
        headerString = """+ (%s)%s:(NSString *)%s
{
    """

        retStr = (headerString % (self.typeName, funcName, self.arg))
        return retStr

    # ----------
    def getFunctionTailToEnum(self):
        retStr = "}\n"
        return retStr


    # ----------
    def getFunctionHeaderStringForEnum(self, funcName):
        headerString = """+ (NSString *)%s:(%s)%s
{
    switch (%s)
    {
    """

        retStr = (headerString % (funcName, self.typeName, self.arg, self.arg))
        return retStr

    # ----------
    def getFunctionTailForEnum(self):
        retStr = """        default:
            return @"--";
    }
    """
        return retStr


    # ----------
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

    # ----------
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

    # ----------
    def generateCodeForStringToEnum(self, funcName, tupList):
        ''' generate the code '''

        retStr = self.getFunctionHeaderStringToEnum(funcName)

        codeList = map( self.genEnumIfPart, tupList )
        retStr += reduce(lambda a, x: a + x, codeList, '' )

        retStr += self.getFunctionTailToEnum()
        return retStr


    # ----------
    def generateCodeForEnumToString(self, funcName, tupList):
        '''
        generate the code
        '''
        retStr = self.getFunctionHeaderStringForEnum(funcName)

        codeList = map( self.genEnumCasePart, tupList )
        retStr += reduce(lambda a, x: a + x, codeList, '' )

        retStr += self.getFunctionTailForEnum()
        return retStr


# -----================------




# --------------- main function - called from stand-alone --------------------------

def main( argv = None ):

    funcFromStringToEnum = "contributionCodeFromString"
    funcFromEnumToString = "stringFromContributionCode"

    inFileName = 'test_input.txt'

    tg = tupGenerator( inFileName )
    tups = tg.getEnumTuples()

    genCode = GenEnumCode( tg.getEnumBaseName(), "code", True )

    function1 = genCode.generateCodeForStringToEnum(funcFromStringToEnum, tups)
    function2 = genCode.generateCodeForEnumToString(funcFromEnumToString, tups)

    print "\n\n----- function1 -----\n", function1
    print "\n\n----- function2 -----\n", function2


# --------------- Run Script as stand-alone --------------------------

if __name__ == "__main__":
    sys.exit(main())

