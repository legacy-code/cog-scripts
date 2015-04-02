#!/usr/bin/env python

"""

Description of the utility.

  usage: %prog [options] args
  -o, --options:           show this screen
  -b, --build=BUILD:       specify the build [Main | R72 | ...]
  
Examples are:

    DwnldBld -D 1
            this will search for the latest build for yesterday (-1 day)

Explanation of the parameters:
========================================

options

    Will show this help.
    
build

    Will show the help for this command and whatever else might be needed.

Other notes:
========================================

Don't have any, but if I did, they'd go here.
    
"""

import sys
import optionparse    # this is in my scripts directory \Mike\scripts

#-------------------------------------------

class UsageError( Exception ):
    def __init__(self, msg):
        self.msg = msg

        
#-------------------------------------------


# ====================================================================
# ====================================================================

        
class MySettings( object ):
    def __init__( self ):
        """
        Will want to put all of the parameters that we are wanting to 
        use in this object.  That way, all the defaults or settings 
        will be in one place.
        """
        pass
        #-------------- Options ---------------
        # set any global or default values here
        
        #-------------------------------------------


def ParseCommandLineArguements( opt, mySets ):
    """
    This method will take the passed in command-line arguements and parse 
    through them, setting values passed in and/or defaulting others.
    
    opt - optionparse object 
            this object contains the command-line options that were passed
            in to the script
            
    mySets - MySettings object
            this object will contain all of the settings and such that need 
            to be set/defaulted to continue with the script
            
    returns:
            NONE - this method does NOT return anything
    
    """

    # -- now default or set things appropriately
    if opt.build:
        # set something here that corresponds to the build option
        #     bld.codeLine = opt.build
        pass
        

    
# ====================================================================
# ====================================================================

# ------------  main function ---------------

def main( argv = None ):
          
    #---- get the command-line options ---------
    opt, args = optionparse.parse( __doc__ )
    if opt.options:
        optionparse.exit()
        
    mySets = MySettings()
        
    ParseCommandLineArguements( opt, mySets )
        
    print "\n\n==============================================================="
    print "Starting to <do whatever>:  \n"
    print "----------------------------------------------------------------"
    print "\n\n"

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        
        # do whatever processing or stuff you need to do here
        pass
        
    except UsageError as err:
        
        print >> sys.stderr, err.msg
        print >> sys.stderr, "error condition"
        return 2
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
          
    print "FINISHED "
    print "===============================================================\n\n"

    
# ====================================================================
# ====================================================================

# --------------- Run Script as stand-alone --------------------------    
    
if __name__ == "__main__":
    sys.exit(main())


    
