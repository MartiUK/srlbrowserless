import curses, scrolllist

stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(1)

stdscr.border(0)
stdscr.refresh()

content = ["The curses library supplies a terminal-independent", "screen-painting and keyboard-handling", "facility for text-based terminals;", "such terminals include VT100s, the Linux", "console, and the simulated terminal", "provided by various programs. Display", "terminals support various", "control codes", "to perform common operations such", "as moving the cursor,", "scrolling the screen, and erasing", "areas. Different terminals", "use widely differing codes, and", "often have their own minor", "quirks.", "The curses library supplies a terminal-independent", "screen-painting and keyboard-handling", "facility for text-based terminals;", "such terminals include VT100s, the Linux", "console, and the simulated terminal", "provided by various programs. Display", "terminals support various", "control codes", "to perform common operations such", "as moving the cursor,", "scrolling the screen, and erasing", "areas. Different terminals", "use widely differing codes, and", "often have their own minor", "quirks."]

y = 2
x = 3

mylist = scrolllist.ScrollList(y, x, curses.LINES-y*2, curses.COLS-x*2, content)
mylist.refresh()

while True:
  cmd = stdscr.getch()
  if cmd == curses.KEY_DOWN:
    mylist.down()
    mylist.refresh()
  elif cmd == curses.KEY_UP:
    mylist.up()
    mylist.refresh()
  if cmd == ord('q'):
    break


stdscr.keypad(0)
curses.echo()
curses.endwin()
