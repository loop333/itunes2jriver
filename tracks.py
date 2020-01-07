#!python3
# -*- coding: utf-8 -*-

from Foundation import *
from ScriptingBridge import *
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

MCWS = "http://localhost:52199/MCWS/v1"

user = "user"
password = "password"

pass_mgr = urllib.request.HTTPPasswordMgrWithPriorAuth()
pass_mgr.add_password(None, MCWS, user, password, is_authenticated=True)
auth_handler = urllib.request.HTTPBasicAuthHandler(pass_mgr)

opener = urllib.request.build_opener(auth_handler)

url = MCWS + "/Authenticate"
resp = opener.open(url)
xml = ET.parse(resp)
e = xml.find("Item[@Name='Token']")
token = e.text

iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")

library = next(x for x in iTunes.sources() if x.name() == "Library")
libraryPlaylist = next(x for x in library.libraryPlaylists() if x.name() == "Library")
tracks = libraryPlaylist.fileTracks()

for track in tracks:
    if track.sampleRate() > 48000 or track.bitRate() > 1500:
#    if track.bpm() == 24 or track.sampleRate() > 48000:
        print(track.album()+": "+track.artist()+" - "+track.name())
        file = urllib.parse.quote(track.location().path())
        url = MCWS + "/Library/Import?Block=1&Token="+token+"&Path="+file
        try:
            resp = urllib.request.urlopen(url)
            d = resp.read().decode("UTF-8")
        except Exception as e:
            print(e)
