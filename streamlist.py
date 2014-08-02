import json, subprocess, urllib2

def getStreams():
  html = urllib2.urlopen('http://api.speedrunslive.com/test/team').read()
  streams = json.loads(html)
  
  for idx, c in enumerate(streams["channels"]):
    tagline = str(idx+1) + ": " + c["channel"]["display_name"] + " - " + c["channel"]["title"].strip()
    if len(tagline) > 80:
      print tagline[0:76] + "..."
    else:
      print tagline
  
  return [x["channel"]["name"] for x in streams["channels"]]

streams = getStreams()
while True:
  index = raw_input("\nEnter stream index, r to refresh, or q to quit: ")
  if index == 'q':
    print "\nClosing..."
    exit()
  elif index == 'r':
    print "\nReloading...\n"
    streams = getStreams()
  else:
    index = int(index) - 1
    url = "twitch.tv/" + streams[index]
    print "\nLoading stream at http://www." + url
    subprocess.call(["livestreamer", url, "best"]) #allow user to select quality
    print "\nStream closed. Reloading...\n"
    streams = getStreams()
