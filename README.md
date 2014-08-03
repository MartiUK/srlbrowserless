# srlbrowserless - 100% unofficial command-line GUI for SpeedRunsLive #

### ABOUT ###

I initially wrote this some time back in late 2013/early 2014 because Flash on Linux is complete garbage, which makes twitch.tv's web player basically unusable (as opposed to "almost unusable" like it is on Windows :^)). For the most part this wasn't a problem for me due to the existence of livestreamer and the fact that I never used twitch's chat or search functions anyway, but at the time I'd been watching a lot of speedruns and was getting sick of having to load SpeedRunsLive in my browser just to see who was running what, so I made this.

Basically what it does is pull the list of runners and games from SRL, then lays everything out in a scrollable list. Once you decide who you want to watch, hitting Enter will take you to quality selection. Make your choice and the stream will (eventually) open up in mpv.

Oh, and you can hit "q" at any time to quit.

### DEPENDANCIES ###

- python
- livestreamer
- mpv (for now)

### TO DO ###

- Add optional command-line arg so the user can choose their own player and pass args through to it
- Display the controls somewhere on the GUI
- Add filtering (the actual website has a filter to cut out trash like MineCraft lmao)
- Figure out why some users' names won't display, then fix it
- Make it so the user can cancel quality selection without quitting the whole program
- (Maybe) add an option so the user can copy the url of the current stream to their clipboard
- (Maybe) make the cursor loop round at the top and bottom
