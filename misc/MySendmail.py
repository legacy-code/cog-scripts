#!/usr/bin/env python

"""

Description of the utility.

   usage: %prog [options] args
   -o, --options:           show this screen
   -s, --sender=SEND:       WHO the email is from (needs to be valid) - required
   -f, --fromMail=FROM:     who email is from (to be authenticated against) - required
   -p, --password=PWD:      password to use for authentication - NOT required
   -t, --to=TO:             the recipients list - required
   -S, --subj=SUBJ:         the subject - required
   -M, --msg=MSG:           the message - required

Examples are:

    %prog -s "me@test.com" -f "Tester@test.com" -t "Me <me@test.com>, You <you@test.com>" -S "test" -M "test message"
            this will send a message from 'me@test.com' with two recipients (me and you).

Explanation of the parameters:
========================================

options

    Will show this help.

sender  (required)

    This is who the email is from.  It needs to be a valid email in the system or it won't actually get sent out.  It
    seems that the server won't fail to try to send it, but something internal to the TDA server checks and will not
    actually send it out.

from  (required)

    This will be who the email shows it's from.  It doesn't appear that it needs to be a valid email, as I've used
    TDABuildAgent@tdameritrade.com, which is NOT a valid email address.
    
password (NOT required)

    This is the password for the "from" account.  

to (required)

    This is the list of emails to send it to (in addition to the sender email).  It should be in one of the following
    forms:
        "Some Name <SomeName@test.com>,Another Name <AnotherName.com>" or
        "somename@test.com,anothername@test.com"

    I think both will work, though, I only remember testing the first one.

subj (required)

    The subject of the email.

msg (required)

    The actual message for the email.  Can be multiline, as long as you package it up correctly to be passed in.


Other notes:
========================================

Not too many right now.  This is using an internal SMTP server on TDA's intra-net and there are no guarantees of how
long it will work.  Currently, there is no need to have to log into the server, except for the notes above for the
sender email.

"""

import sys
import optionparse    # this is in my scripts directory \Mike\scripts

#-------------------------------------------

class UsageError( Exception ):
    def __init__(self, msg):
        self.msg = msg


class NotAllParametersSpecified( Exception ):
    def __init__(self,msg):
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

        self.sender = ""
        self.fromMail = ""
        self.password = ""
        self.to = ""
        self.subj = "Test Message"
        self.msg = "Test message body"
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
    if opt.sender:
        mySets.sender = opt.sender

    if opt.fromMail:
        mySets.fromMail = opt.fromMail
        
    if opt.password:
        mySets.password = opt.password

    if opt.to:
        mySets.to = opt.to

    if opt.subj:
        mySets.subj = opt.subj

    if opt.msg:
        mySets.msg = opt.msg




# ====================================================================
# ====================================================================

# ------------  main function ---------------

import smtplib
import email.utils
from email.mime.text import MIMEText


def main( argv = None ):

    #---- get the command-line options ---------
    opt, args = optionparse.parse( __doc__ )
    if opt.options:
        optionparse.exit()

    mySets = MySettings()

    ParseCommandLineArguements( opt, mySets )

    print "\n\n==============================================================="
    print "Starting to send a message:  \n"
    print "----------------------------------------------------------------"
    print "\n\n"

    retVal = 0

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:

        # check to make sure that we have all the parameters
        if mySets.sender == "" or \
                mySets.fromMail == "" or \
                mySets.to == ""     or mySets.subj == "" or mySets.msg == "":
            # we didn't get all of the parameters we needed
            raise NotAllParametersSpecified("Required parameters are missing")

        # Create the message
        msg = MIMEText(mySets.msg)
        msg['To'] = mySets.to
        msg['Subject'] = mySets.subj

        # this is the TDA smtp server that I know about
        #server = smtplib.SMTP('10.134.7.15')
        server = smtplib.SMTP('prdctavmgwhst03.associatesys.local')
        server.set_debuglevel(True) # show communication with the server

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

        if mySets.password != "":
            try:
                print >> sys.stderr, "Password proviced, so attempting to log in!"
                server.login(mySets.fromMail, mySets.password)
            except:
                print >> sys.stderr, "ERROR with logging in."
        
        fromMail = mySets.fromMail
        toMail = mySets.to

        try:
            server.sendmail(fromMail, [toMail, fromMail], msg.as_string())
        finally:
            print >> sys.stderr, "Attempting to quit the SMTP server now."
            server.quit()

    except (UsageError, NotAllParametersSpecified) as err:
        print >> sys.stderr, "\n\n"
        print >> sys.stderr, err.msg
        print >> sys.stderr, "error condition"
        print >> sys.stderr, "\n\n"
        retVal = 2
    except smtplib.SMTPRecipientsRefused as err:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPRecipientsRefused error"
        print >> sys.stderr, err.recipients
        print >> sys.stderr, "\n\n"
        retVal = 4
    except smtplib.SMTPException:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPException error!\n\n"
        retVal = 50
    except smtplib.SMTPServerDisconnected:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPServerDisconnected error!\n\n"
        retVal = 51
    except smtplib.SMTPResponseException:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPResponseException error!\n\n"
        retVal = 52
    except smtplib.SMTPSenderRefused:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPSenderRefused error!\n\n"
        retVal = 53
    except smtplib.SMTPDataError:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPDataError error!\n\n"
        retVal = 54
    except smtplib.SMTPConnectError: 
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPConnectError error!\n\n"
        retVal = 55
    except smtplib.SMTPHeloError: 
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPHeloError error!\n\n"
        retVal =56
    except smtplib.SMTPAuthenticationError:
        print >> sys.stderr, "\n\nUnexpected SMTPLib SMTPAuthenticationError error!\n\n"
        retVal = 57
    except:
        print >> sys.stderr, "\n\nUnexpected error!\n\n"
        e = sys.exc_info()[0]
        print e
        retVal = 100
        

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++

    print "\n\nFINISHED "
    print "===============================================================\n\n"

    return retVal

# ====================================================================
# ====================================================================

# --------------- Run Script as stand-alone --------------------------

if __name__ == "__main__":
    sys.exit(main())



