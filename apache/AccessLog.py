import fileinput
import re
import os
try: import simplejson as json
except ImportError: import json

#read input file and return entries' Dict Object
def readfile(file, marshall=False):
    filecontent = []
    index = 0
    #check necessary file size checking
    statinfo = os.stat(file)

    #just a guestimate. I believe a single entry contains atleast 150 chars
    if statinfo.st_size < 150:
        print("Not a valid access_log file. It does not have enough data")
    else:
        for line in fileinput.input(file):
            index = index+1
            if line != "\n": #don't read newlines
                filecontent.append(line2dict(line, marshall))

        fileinput.close()
    return filecontent

#gets a line of string from Log and convert it into Dict Object
def line2dict(line, marshall):
    #Snippet, thanks to http://www.seehuhn.de/blog/52
    parts = [
    r'(?P<HOST>\S+)',                   # host %h
    r'(?P<IDENTITY>\S+)',               # indent %l (unused)
    r'(?P<USER>\S+)',                   # user %u
    r'\[(?P<TIME>.+)\]',                # time %t
    r'"(?P<REQUEST>.+)"',               # request "%r"
    r'(?P<STATUS>[0-9]+)',              # status %>s
    r'(?P<SIZE>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<REFERER>.*)"',               # referer "%{Referer}i"
    r'"(?P<USERAGENT>.*)"',                 # user agent "%{User-agent}i"
]
    pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')
    m = pattern.match(line)
    import sys
    res = m.groupdict()

    if(marshall):
        res2 = {}
        for k in res :
            t = 'S'
            if(re.search(r'STATUS|SIZE', k, flags=re.IGNORECASE)):
                t = 'N'
            res2[k] = {}
            res2[k][t] = res[k]
        return res2
        
    return res

#to get jSon of entire Log
#returns JSON object
def toJson(file, marshall=False):
    #get dict object for each entry
    entries = readfile(file, marshall)
    return json.JSONEncoder().encode(entries)

    
