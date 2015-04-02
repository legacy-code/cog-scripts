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


/*[[[cog
import cog
fnames = ['DoSomething', 'DoAnotherThing', 'DoLastThing']
for fn in fnames:
    cog.outl("void %s();" % fn)
]]]*/
//[[[end]]]


