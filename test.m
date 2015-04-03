// This is my C++/Objective-C file.

// some comments


enum months {Jan, Feb, Mar, Apr, May, Jun, July, Aug, Sept, Oct, Nov, Dec};
enum months currentMonth;


enum weight {slim = 120, medium= 140, stocky = 160};
enum weight currentWeight;
int currentWeight = medium;
NSLog (@"The Current Weight is %i pounds", currentWeight);


typedef NS_ENUM(NSInteger, UITableViewCellStyle) {
        UITableViewCellStyleDefault,
        UITableViewCellStyleValue1,
        UITableViewCellStyleValue2,
        UITableViewCellStyleSubtitle
};


typedef NS_ENUM(NSInteger, UITableViewCellStyle)
{
        UITableViewCellStyleDefault     = 1,
        UITableViewCellStyleValue1      = 2,
        UITableViewCellStyleValue2      = 3,
        UITableViewCellStyleSubtitle    = 4
};


typedef NS_ENUM(NSUInteger, TDAIRAContributionCode)
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
    TDAIRAContributionCodeC20 = 20
};


/*[[[cog
import cog
fnames = ['DoSomething', 'DoAnotherThing', 'DoLastThing']
for fn in fnames:
    cog.outl("void %s();" % fn)
]]]*/
//[[[end]]]


