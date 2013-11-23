# converts subtitles from Timed Text Markup Language (TTML) to SubRip (SRT)

import xbmc, os
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from HTMLParser import HTMLParser

class SubtitleConverter(HTMLParser):
    "Convert TTML subtitles to SubRip (SRT) subtitles"
    counter = 0
    text = ""
    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.counter += 1
            if self.counter > 1:
                self.text += "\n\n" + str(self.counter) + "\n"
            else:
                self.text += str(self.counter) + "\n"
            for name, value in attrs:
                if name == 'begin':
                    if len(value) < 6:
                        self.text += "0:" + value + ",0 --> "
                    else:
                        self.text += value + ",0 --> "
                if name == 'end':
                    if len(value) < 6:
                        self.text += "0:" + value + ",0\n"
                    else:
                        self.text += value + ",0\n"
        elif tag == "br":
            self.text += "\n"
    def handle_data(self, data):
        s = data.strip()
        if s <> "":
            self.text += s

def ttml2srt(ttml, name):
    parser = SubtitleConverter()
    parser.feed(ttml)
    srt = parser.text
    
    print "----- saving"
    tmp_dir = xbmc.translatePath( "special://temp")
    #tmp_dir = "d:\\temp\\"
    subs = os.path.join(tmp_dir, 'serialepenet')
    if os.path.isdir(subs) is False:
        os.makedirs(subs)
    tmp_file = subs + os.sep + name
    print tmp_file
    f = open(tmp_file, 'w')
    f.write(srt)
    f.close()

    return tmp_file

def extract_subtitle(url, filename, useragent):
    headers = {'User-Agent': useragent}
    print "--- getting subtitle file"
    r = requests.get(url, headers = headers)
    print "--- done"
    text = r.content.strip()
    if text.startswith("<tt"):
        print "--- converting subtitles"
        subt = ttml2srt(text, filename)
        print "--- done: ", subt
    else:
        print "--- subtitle in correct format, saving"
        tmp_dir = xbmc.translatePath("special://temp")
        subs = os.path.join(tmp_dir, 'serialepenet')
        if os.path.isdir(subs) is False:
            os.makedirs(subs)
        tmp_file = subs + os.sep + filename
        print tmp_file
        f = open(tmp_file, 'w')
        f.write(text)
        f.close()
        subt = tmp_file

    return subt
