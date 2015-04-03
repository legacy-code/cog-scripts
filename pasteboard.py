#!/usr/bin/python

# http://pastebin.com/4MjuSkW3
# __author__ = 'unknown - in pastebin'

from Foundation import *
#from AppKit import
import AppKit


def pbcopy(s):
    "Copy string argument to clipboard"
    board = AppKit.NSPasteboard.generalPasteboard()
    board.declareTypes_owner_([AppKit.NSStringPboardType], None)
    newStr = Foundation.NSString.stringWithString_(s)
    newData = \
        newStr.nsstring().dataUsingEncoding_(Foundation.NSUTF8StringEncoding)
    board.setData_forType_(newData, AppKit.NSStringPboardType)

def pbpaste():
    "Returns contents of clipboard"
    board = AppKit.NSPasteboard.generalPasteboard()
    content = board.stringForType_(AppKit.NSStringPboardType)
    return content

class PasteBoard(object):
    def copy(self, s):
        if not isinstance(s, basestring):
            s = repr(s)
        pbcopy(s)
    paste = property(lambda self: pbpaste(), fset=copy)
    copy = property(lambda self: pbpaste(), fset=copy)

    def lines():
        def fget(self):
            return pbpaste().replace("\r","\n").split("\n")

        def fset(self, l):
            pbcopy('\n'.join(unicode(i) for i in l))

        return {'fget':fget, 'fset':fset}
    lines = property(**lines())

    def split():
        def fget(self):
            def _(sep):
                return pbpaste().replace("\r"," ").replace("\n"," ").split(sep)
            return _

        def fset(self, t):
            pbcopy(unicode(t[0]).join(unicode(i) for i in t[1]))

        return {'fget':fget, 'fset':fset}
    split = property(**split())
    join = split

    def words():
        def fget(self):
            return pbpaste().replace("\r"," ").replace("\n"," ").split(" ")

        def fset(self, l):
            pbcopy(' '.join(unicode(i) for i in l))

        return {'fget':fget, 'fset':fset}
    words = property(**words())

    def to_plain(self):
        pbcopy(pbpaste())

    def to_ascii(self):
        pbcopy(pbpaste().encode("ASCII", "ignore"))

    def to_nonascii(self):
        pbcopy(''.join(char for char in pbpaste() if ord(char)>128))

    def to_indent(self):
        pbcopy('\n'.join('\t'+line for line in pbpaste().split("\n")))

    def to_dedent(self):
        lines = pbpaste().replace("\t", "    ").split("\n")
        lines = '\n'.join(line[4:] for line in lines)
        pbcopy(lines)

    def to_title(self):
        pbcopy(pbpaste().title())

pb = PasteBoard()