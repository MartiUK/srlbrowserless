#!/usr/bin/env python

import argparse
import curses
import HTMLParser
import json
import livestreamer
import locale
import re
import scrolllist
import subprocess
import urllib2

# get all the streams, return a tuple of [tagline, name]


def getStreams(length):
    html = urllib2.urlopen('http://api.speedrunslive.com/test/team').read()
    streamsraw = json.loads(html)

    streams = []
    h = HTMLParser.HTMLParser()
    for idx, c in enumerate(streamsraw["channels"]):
        tagline = str(idx + 1) + ": " + c["channel"][
            "display_name"] + " - " + c["channel"]["title"].strip()
        tagline = h.unescape(tagline)
        if len(tagline) > length:
            tagline = tagline[0:length - 3] + "..."
        streams.append({"tagline": tagline, "name": c["channel"]["name"]})

    # add filtering to this to match up with the site itself

    return streams

# get a list of available qualities for a given streamer, or raise if the
# streamer is offline


def getQualities(url):
    streams = livestreamer.streams(url)
    if not streams == {}:
        qualities = []
        for idx, l in enumerate(streams.keys()):
            qualities.append(
                {"label": str(idx + 1) + ": " + l.capitalize(), "quality": l})
        return qualities
    else:
        raise

# not used right now


def printError(message):
    f = open("streamlistgui.log", "w")
    f.write(message)
    f.close()

# used to redraw listwin w/ a message since it happens a lot


def redraw(window, message=None, h=0, w=0):
    window.erase()
    window.border(0)
    if message != None:
        window.addstr(h / 2, (w - len(message)) / 2, message)
    window.refresh()

# load and redraw the stream list, return it and the list of streams


def loadStreams(yoffset, xoffset, padh, padw):
    streams = getStreams(padw)
    streamlist = scrolllist.ScrollList(
        yoffset, xoffset, padh, padw, [x["tagline"] for x in streams])
    streamlist.refresh()
    return [streams, streamlist]

# get some args
parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--player", help="shell command for your chosen player, including any arguments you wish to pass forward (defaults to vlc if available)")
args = parser.parse_args()

# make sure people with stupid characters in their names don't crash the thing
locale.setlocale(locale.LC_ALL, "")

# initialise gui
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(0)
stdscr.keypad(1)

# draw some stuff
stdscr.border(0)
stdscr.addstr(0, (curses.COLS / 2) - 24,
              "SpeedRunsLive Unofficial Command-Line GUI Alpha")
stdscr.refresh()

# get these distances right
xoffset = 3
yoffset = 2
padw = curses.COLS - xoffset * 2
padh = curses.LINES - yoffset * 2

# draw the window so we get a ~nice border~
listwin = curses.newwin(
    yoffset + padh, xoffset + padw - 1, yoffset - 1, xoffset - 1)
# need win-1, so use pad dims cos they're win-1
redraw(listwin, "Loading stream list...", padh, padw)

# initialise the list
streams, streamlist = loadStreams(yoffset, xoffset, padh, padw)
redraw(listwin)
streamlist.refresh()

# control logic
streamselection = True
while True:
    cmd = stdscr.getch()
    if streamselection:
        if cmd == curses.KEY_DOWN:
            streamlist.down()
            streamlist.refresh()
        elif cmd == curses.KEY_UP:
            streamlist.up()
            streamlist.refresh()
        elif cmd == ord("\n"):
            url = "twitch.tv/" + streams[streamlist.getindex()]["name"]
            # if the stream is up, let the user select a quality
            # otherwise reload stream list cos it's probably out of date
            try:
                qualities = getQualities(url)
            except:
                # don't need to delete streamlist here since we're just
                # reinitialising
                redraw(listwin)
                streams, streamlist = loadStreams(yoffset, xoffset, padh, padw)
            else:
                # could probably get away with not deleting it here but w/e
                # it's memory shit
                del streamlist
                redraw(listwin)
                qualitylist = scrolllist.ScrollList(
                    yoffset, xoffset, padh, padw, [x["label"] for x in qualities])
                qualitylist.refresh()
                streamselection = False
        elif cmd == ord("r"):
            streams, streamlist = loadStreams(yoffset, xoffset, padh, padw)
        elif cmd == ord("q"):
            break
    else:
        if cmd == curses.KEY_DOWN:
            qualitylist.down()
            qualitylist.refresh()
        elif cmd == curses.KEY_UP:
            qualitylist.up()
            qualitylist.refresh()
        elif cmd == ord("\n"):
            quality = qualities[qualitylist.getindex()]["quality"]
            # clean up the window before showing the stream
            del qualitylist
            redraw(listwin, "Now viewing: " + url, padh, padw)
            cmd = ["livestreamer", "-Q"]
            if args.player:
                cmd += ["-p", args.player]
            cmd += [url, quality]
            subprocess.call(cmd)
            streams, streamlist = loadStreams(yoffset, xoffset, padh, padw)
            streamselection = True
        elif cmd == ord("q"):
            break

# shut the club down
stdscr.keypad(0)
curses.curs_set(2)
curses.echo()
curses.endwin()
