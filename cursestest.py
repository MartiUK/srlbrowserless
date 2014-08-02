import curses, math

#initialise gui
stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(1)

stdscr.border(0)
stdscr.addstr(0,0, "SpeedRunsLive Unofficial Command-Line GUI Alpha")
stdscr.refresh()

streams = ["The curses library supplies a terminal-independent", "screen-painting and keyboard-handling", "facility for text-based terminals;", "such terminals include VT100s, the Linux", "console, and the simulated terminal", "provided by various programs. Display", "terminals support various", "control codes", "to perform common operations such", "as moving the cursor,", "scrolling the screen, and erasing", "areas. Different terminals", "use widely differing codes, and", "often have their own minor", "quirks.", "The curses library supplies a terminal-independent", "screen-painting and keyboard-handling", "facility for text-based terminals;", "such terminals include VT100s, the Linux", "console, and the simulated terminal", "provided by various programs. Display", "terminals support various", "control codes", "to perform common operations such", "as moving the cursor,", "scrolling the screen, and erasing", "areas. Different terminals", "use widely differing codes, and", "often have their own minor", "quirks."]

#get these distances right
xoffset = 3
yoffset = 2
mypadw = curses.COLS-xoffset*2
mypadh = curses.LINES-yoffset*2

mypad = curses.newpad(len(streams), mypadw)
for idx, l in enumerate(streams):
  mypad.addstr(idx, 0, l)

#set cursor pos to 0
mypadpos = 0
index = 0
mypad.addstr(0, 0, streams[0], curses.A_REVERSE)

#draw
mypad.refresh(mypadpos, 0, yoffset, xoffset, yoffset+mypadh-1, xoffset+mypadw-1)

#control logic
while True:
  cmd = stdscr.getch()
  if cmd == curses.KEY_DOWN:
    if index < len(streams)-1:
      mypad.addstr(index, 0, streams[index])
      index += 1
      mypad.addstr(index, 0, streams[index], curses.A_REVERSE)
      if (index >= mypadh/2) & (index < len(streams) - math.ceil(mypadh/2.0)):
        mypadpos += 1
      stdscr.addstr(0, 0, str(index) + ", " + str(mypadpos))
  elif cmd == curses.KEY_UP:
    if index > 0:
      #somehow putting this here works?? i think it skips an extra math.ceil() so w/e
      if (index >= mypadh/2) & (index < len(streams) - math.ceil(mypadh/2.0)):
        mypadpos -= 1
      mypad.addstr(index, 0, streams[index])
      index -= 1
      mypad.addstr(index, 0, streams[index], curses.A_REVERSE)
      stdscr.addstr(0, 0, str(index) + ", " + str(mypadpos))
  elif cmd == ord('q'):
    break
  mypad.addstr(index, 0, streams[index], curses.A_REVERSE)
  mypad.refresh(mypadpos, 0, yoffset, xoffset, yoffset+mypadh-1, xoffset+mypadw-1)

#shut the club down
stdscr.keypad(0)
curses.echo()
curses.endwin()
