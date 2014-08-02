import curses, math

#scrolling ncurses list
#note: this thing does NOT refresh itself at any point: that's up to the user via .refresh()
class ScrollList:
  #height refers to displayed area while length refers to the length of the list itself
  def __init__(self, yoffset, xoffset, height, width, content):
    self.y = yoffset
    self.x = xoffset
    self.height = height
    self.width = width
    self.length = len(content)
    self.toplimit = math.ceil(height/2.0)-1 #scroll mode switches at this index and beyond
    self.bottomlimit = height/2+1 #scroll mode switches back past this index
    self.index = 0
    self.pad = curses.newpad(self.length, width)
    self.padpos = 0
    
    #populate list
    for idx, l in enumerate(content):
      #for some stupid reason curses raises an error on writing to the bottom rightmost cell
      try:
        self.pad.addstr(idx, 0, l.encode("utf-8"))
      except curses.error:
        pass
    
    #highlight the first line
    self.pad.chgat(0, 0, curses.A_REVERSE)
  
  def up(self):
    if self.index > 0:
      #change index and move highlight
      self.pad.chgat(self.index, 0, curses.A_NORMAL)
      self.index -= 1
      self.pad.chgat(self.index, 0, curses.A_REVERSE)
      #scroll the pad itself while index falls between the top and bottom limits
      if (self.index >= self.toplimit) & (self.index < self.length-self.bottomlimit):
        self.padpos -= 1
  
  def down(self):
    if self.index < self.length-1:
      #change index and move highlight
      self.pad.chgat(self.index, 0, curses.A_NORMAL)
      self.index += 1
      self.pad.chgat(self.index, 0, curses.A_REVERSE)
      #scroll the pad itself while index falls between the top and bottom limits
      if (self.index > self.toplimit) & (self.index <= self.length-self.bottomlimit):
        self.padpos += 1
  
  def getindex(self):
    return self.index
  
  def refresh(self):
    self.pad.refresh(self.padpos, 0, self.y, self.x, self.y+self.height-1, self.x+self.width-1)
