#!/usr/bin/env python
"""\
:Author: M. Simionato
:Date: April 2004
:Title: A much simplified interface to optparse.

Title: Parsing the command line
Submitter: Michele Simionato (other recipes)
Last Updated: 2004/04/18
Version no: 1.1
Category: System 
http://code.activestate.com/recipes/278844/
https://urldefense.proofpoint.com/v1/url?u=http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278844&k=%2FJMyfAnQZOhZ4dnr8BYv6w%3D%3D%0A&r=xfKu0iWVBjTdoA22PB9jOqI%2FucON8dpuy3toOQYqQ%2Fc%3D%0A&m=QOBZQ8%2BM%2Bd9K6iaU%2FdWubH8rlpQNYPXz26wby16JneU%3D%0A&s=652fdf98b2446511c6a8d19c697a2590fd7cefcfb77a563c4432528510d682a1

You should use optionparse in your scripts as follows.
First, write a module level docstring containing something like this
(this is just an example):

'''usage: %prog files [options]
   -d, --delete: delete all files
   -e, --erase = ERASE: erase the given file'''
   
Then write a main program of this kind:

# sketch of a script to delete files
if __name__=='__main__':
    import optionparse
    option,args=optionparse.parse(__doc__)
    if not args and not option: optionparse.exit()
    elif option.delete: print "Delete all files"
    elif option.erase: print "Delete the given file"

Notice that ``optionparse`` parses the docstring by looking at the
characters ",", ":", "=", "\\n", so be careful in using them. If
the docstring is not correctly formatted you will get a SyntaxError
or worse, the script will not work as expected.
"""

import optparse, re, sys

USAGE = re.compile(r'(?s)\s*usage: (.*?)(\n[ \t]*\n|$)')

def nonzero(self): # will become the nonzero method of optparse.Values       
    "True if options were given"
    for v in self.__dict__.itervalues():
        if v is not None: return True
    return False

optparse.Values.__nonzero__ = nonzero # dynamically fix optparse.Values

class ParsingError(Exception): pass

optionstring=""

def exit(msg=""):
    raise SystemExit(msg or optionstring.replace("%prog",sys.argv[0]))

def parse(docstring, arglist=None):
    global optionstring
    optionstring = docstring
    match = USAGE.search(optionstring)
    if not match: raise ParsingError("Cannot find the option string")
    optlines = match.group(1).splitlines()
    try:
        p = optparse.OptionParser(optlines[0])
        for line in optlines[1:]:
            opt, help=line.split(':')[:2]
            short,long=opt.split(',')[:2]
            if '=' in opt:
                action='store'
                long=long.split('=')[0]
            else:
                action='store_true'
            p.add_option(short.strip(),long.strip(),
                         action = action, help = help.strip())
    except (IndexError,ValueError):
        raise ParsingError("Cannot parse the option string correctly")
    return p.parse_args(arglist)
