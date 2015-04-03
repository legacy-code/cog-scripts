#!/usr/bin/python


input='''typedef NS_ENUM(NSUInteger, TDAIRAContributionCode)
{
    TDAIRAContributionCodeUnknown = 0,
    TDAIRAContributionCodeC1 = 1,   // IRA Contribution Current Year
    TDAIRAContributionCodeC2 = 2,   // IRA Contribution Previous Year
    TDAIRAContributionCodeC3 = 3,   // Employer SEP Contribution
    TDAIRAContributionCodeC4 = 4,
    TDAIRAContributionCodeC5 = 5,   // 60-Day Rollover
    TDAIRAContributionCodeC6 = 6,
    TDAIRAContributionCodeC7 = 7,
    TDAIRAContributionCodeC8 = 8,
    TDAIRAContributionCodeC9 = 9,
    TDAIRAContributionCodeC10 = 10,
    TDAIRAContributionCodeC11 = 11,
    TDAIRAContributionCodeC12 = 12,
    TDAIRAContributionCodeC13 = 13,
    TDAIRAContributionCodeC14 = 14, // Roth Contribution Current Year
    TDAIRAContributionCodeC15 = 15, // Roth Contribution Previous Year
    TDAIRAContributionCodeC16 = 16, // Education IRA Contribution Current Year
    TDAIRAContributionCodeC17 = 17,  // Education IRA Contribution Previous Year
    TDAIRAContributionCodeC18 = 18,
    TDAIRAContributionCodeC19 = 19,
    TDAIRAContributionCodeC20 = 20  // test comment
};
'''

def getEnumBaseName( inDict ):
    retStr = ""
    for line in inDict:
        if line.find("NS_ENUM") != -1:
            temp = line.split(',')
            retStr = temp[1].replace(")", "").strip()
            return retStr

    return retStr

def getEnumTuples( inDict ):
    retList = list()

    baseName = getEnumBaseName( inDict )

    for line in inDict:
        if line.find(" = ") != -1:
            strName = ""
            idNum = ""
            comment = ""

            tupleList = line.split(" = ")
            strName = tupleList[0].replace(baseName, "").strip()
            if tupleList[1].find( "//" ) >= 0:
                tupleList = tupleList[1].split('//')
            else:
                tupleList = tupleList[1].split(',')
                if len(tupleList) >= 2:
                    tupleList[1].replace('//', '')

            idNum = tupleList[0]
            if len(tupleList) >= 2:
                comment = tupleList[1]

            retList.append( (strName, idNum, comment) )

    return retList


# -----================------

def generateCodeForStringToEnum(funcName, arg, typeName, tupList):
    ''' generate the code '''

    headerString = """+ (%s)%s:(NSString *)%s
{
    """

    retStr = (headerString % (typeName, funcName, arg))

    firstItem = True
    for tup in tupList:
        retStr += genEnumIfPart(firstItem, typeName, arg, tup)
        if firstItem:
            firstItem = False

    retStr += "}\n"

    return retStr




def genEnumIfPart( firstItem, typeName, arg, tup ):
    """
    """
    retStr = ""
    formatStr = '''%sif ([%s isEqualToString:@"%s"])
    {
        return %s%s;
    }
    '''

    eClause = "else "
    if firstItem:
        eClause = ""

    retStr = (formatStr % (eClause, arg, tup[0], typeName, tup[0] ))

    return retStr

# -----================------


def generateCodeForEnumToString(funcName, arg, typeName, tupList):
    '''
    generate the code

       switch (code) {
        case TDAIRAContributionCodeC1:
            return @"C1";
    '''

    headerString = """+ (NSString *)%s:(%s)%s
{
    switch (%s)
    {
    """

    retStr = (headerString % (funcName, typeName, arg, arg))

    firstItem = True
    for tup in tupList:
        retStr += genEnumCasePart(typeName, arg, tup)
        if firstItem:
            firstItem = False

    retStr += """        default:
            return @"--";
    }
    """

    return retStr




def genEnumCasePart( typeName, arg, tup ):
    """
    case TDAIRAContributionCodeC1:
            return @"C1";
    """
    retStr = ""
    formatStr = '''case %s%s:
        return @"%s";
    '''

    retStr = (formatStr % (typeName, tup[0], tup[0] ))

    return retStr

# -----================------




def main():

    # check to see that can get the correct base name
    inD = input.split('\n')

    baseName = getEnumBaseName(inD)

    funcFromStringToEnum = "contributionCodeFromString"
    funcFromEnumToString = "stringFromContributionCode"

    tupList = getEnumTuples( inD )
    printIterable(tupList, "Tuple List for enum")

    function1 = generateCodeForStringToEnum( funcFromStringToEnum, "code", baseName, tupList )
    function2 = generateCodeForEnumToString( funcFromEnumToString, "code", baseName, tupList )

    print function1
    print function2


def printIterable( it, title ):
    print "\n"
    print title
    for i in it:
        print i
    print "\n"


if __name__ == "__main__":
    main()

expectedOutput = '''
+ (TDAIRAContributionCode)contributionCodeFromString:(NSString *)code
{
    if (!code)
    {
        return TDAIRAContributionCodeUnknown;
    }

    if ([code isEqualToString:@"C1"])
    {
        return TDAIRAContributionCodeC1;
    }
    else if ([code isEqualToString:@"C2"])
    {
        return TDAIRAContributionCodeC2;
    }
    else if ([code isEqualToString:@"C3"])
    {
        return TDAIRAContributionCodeC3;
    }
    else if ([code isEqualToString:@"C4"])
    {
        return TDAIRAContributionCodeC4;
    }
    else if ([code isEqualToString:@"C5"])
    {
        return TDAIRAContributionCodeC5;
    }
    else if ([code isEqualToString:@"C6"])
    {
        return TDAIRAContributionCodeC6;
    }
    else if ([code isEqualToString:@"C7"])
    {
        return TDAIRAContributionCodeC7;
    }
    else if ([code isEqualToString:@"C8"])
    {
        return TDAIRAContributionCodeC8;
    }
    else if ([code isEqualToString:@"C9"])
    {
        return TDAIRAContributionCodeC9;
    }
    else if ([code isEqualToString:@"C10"])
    {
        return TDAIRAContributionCodeC10;
    }
    else if ([code isEqualToString:@"C11"])
    {
        return TDAIRAContributionCodeC11;
    }
    else if ([code isEqualToString:@"C12"])
    {
        return TDAIRAContributionCodeC12;
    }
    else if ([code isEqualToString:@"C13"])
    {
        return TDAIRAContributionCodeC13;
    }
    else if ([code isEqualToString:@"C14"])
    {
        return TDAIRAContributionCodeC14;
    }
    else if ([code isEqualToString:@"C15"])
    {
        return TDAIRAContributionCodeC15;
    }
    else if ([code isEqualToString:@"C16"])
    {
        return TDAIRAContributionCodeC16;
    }
    else if ([code isEqualToString:@"C17"])
    {
        return TDAIRAContributionCodeC17;
    }
    else if ([code isEqualToString:@"C18"])
    {
        return TDAIRAContributionCodeC18;
    }
    else if ([code isEqualToString:@"C19"])
    {
        return TDAIRAContributionCodeC19;
    }
    else if ([code isEqualToString:@"C20"])
    {
        return TDAIRAContributionCodeC20;
    }
    else
    {
        return TDAIRAContributionCodeUnknown;
    }
}

+ (NSString *)stringFromContributionCode:(TDAIRAContributionCode)code
{
    switch (code) {
        case TDAIRAContributionCodeC1:
            return @"C1";
        case TDAIRAContributionCodeC2:
            return @"C2";
        case TDAIRAContributionCodeC3:
            return @"C3";
        case TDAIRAContributionCodeC4:
            return @"C4";
        case TDAIRAContributionCodeC5:
            return @"C5";
        case TDAIRAContributionCodeC6:
            return @"C6";
        case TDAIRAContributionCodeC7:
            return @"C7";
        case TDAIRAContributionCodeC8:
            return @"C8";
        case TDAIRAContributionCodeC9:
            return @"C9";
        case TDAIRAContributionCodeC10:
            return @"C10";
        case TDAIRAContributionCodeC11:
            return @"C11";
        case TDAIRAContributionCodeC12:
            return @"C12";
        case TDAIRAContributionCodeC13:
            return @"C13";
        case TDAIRAContributionCodeC14:
            return @"C14";
        case TDAIRAContributionCodeC15:
            return @"C15";
        case TDAIRAContributionCodeC16:
            return @"C16";
        case TDAIRAContributionCodeC17:
            return @"C17";
        case TDAIRAContributionCodeC18:
            return @"C18";
        case TDAIRAContributionCodeC19:
            return @"C19";
        case TDAIRAContributionCodeC20:
            return @"C20";
        case TDAIRAContributionCodeUnknown:
        default:
            return @"--";
    }
}
'''
