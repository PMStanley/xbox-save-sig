#Copyright (c) <2015> <Pete Stanley>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import hashlib, hmac
import sys, getopt
from struct import *

def usage():
    print("xboxsig.py -i <xbe file> // prints key in native format")
    print("xboxsig.py -i <xbe file> -t // prints key in native format and includes game title")
    print("xboxsig.py -i <xbe file> -o <outputfile.txt> //outputs key in ascii to specificed file")
    print("xboxsig.py -g <game sig in text form> //generate key from input text rather than xbe file")
    print("xboxsig.py -i <xbe file> -f <native|raw|xbtf> //prints out key in specified format, default is native if this paramenter is not used.")

def main():
    #figure out if we're using Python 2
    PY2 = sys.version_info[0] == 2

    #set the default xbox key and some other base values
    xboxkey = '5C0733AE0401F7E8BA7993FDCD2F1FE0'
    fileOutput = False
    title = None
    includeTitle = False
    format = 'native'

    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:g:x:o:f:t",["xbe=","gamesig=","xboxkey=","outfile=", "format=", "title"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    #no args?  Display some usage examples and quit
    if len(opts) == 0:
        usage()
        sys.exit(2)

    #work through the supplied arguments..
    for opt, arg in opts:
        if opt in ("-x", "--xboxkey"):
            xboxkey = arg

        elif opt in ("-o", "--outfile"):
            outputfile = arg
            fileOutput = True

        elif opt in ("-i", "--xbe"):
            xbeKey, title = getKeyfromXBE(arg)

        elif opt in ("-g", "--gamesig"):
            if PY2:
                xbeKey = arg.decode("hex")
            else:
                xbeKey = bytes.fromhex(arg)

        elif opt in ("-t", "--title"):
            includeTitle = True

        elif opt in ("-f", "--format"):
            if arg.lower() == 'xbtf':
                format = 'xbtf'
            elif arg.lower() == 'native':
                format = 'native'
            elif arg.lower() == 'raw':
                format = 'raw'


    #generate the signing key
    if PY2:
        sigKey = generateKey(xboxkey.decode("hex"), xbeKey)
    else:
        sigKey = generateKey(bytes.fromhex(xboxkey), xbeKey)


    #output the key in the desired format
    if fileOutput:
        of = open(outputfile, "w")
        try:
            if (includeTitle) and (title is not None):
                of.write(title + "\n")
            #Xbox length
            of.write(formatSigKey(sigKey, format))
        finally:
            of.close
    else:
        #write it out to the console instead
        if (includeTitle) and (title is not None):
            print(title)
        print(formatSigKey(sigKey, format))


def getKeyfromXBE(xbefile):
    f = open(xbefile, "rb")
    try:
        #move to base address
        f.seek(260, 0)
        base = f.read(4)

        #move to cert address
        f.seek(280,0)
        cert = f.read(4)

        #get the location of the cert
        certAddress = unpack("i", cert)
        baseAddress = unpack("i", base)
        loc = certAddress[0] - baseAddress[0]

        #move to the title
        f.seek(loc + 12, 0)
        gameTitle = f.read(128)

        #move to the sigkey
        f.seek(loc + 192, 0)
        m_sig_key = f.read(16)

    finally:
        f.close()
        return m_sig_key, gameTitle


def generateKey(xkey, gkey):
    sigKey = hmac.new(xkey, gkey, hashlib.sha1)
    return sigKey.hexdigest()

def formatSigKey(rawsig, formatting):
    if formatting == 'native':
        return rawsig[:32].upper()

    elif formatting == 'raw':
        return rawsig.upper()

    elif formatting == 'xbtf':
        returnstring = ''
        y = 0
        for x in range(0,15):
            returnstring = returnstring + '0x' + rawsig[y:y+2] +  ', '
            y = y + 2
        returnstring = returnstring + '0x' + rawsig[y:y+2]
        return returnstring.upper()


if __name__ == "__main__":
    main()
