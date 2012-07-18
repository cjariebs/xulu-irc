import curses

def init():
	global stdscr
	stdscr = curses.initscr()
	curses.cbreak()
	curses.noecho()

	size = stdscr.getmaxyx()
	global outwin, cmdwin, cmdstr, lines
	outwin = curses.newwin(size[0]-1, size[1], 0, 0)
	cmdwin = curses.newwin(1, size[1], size[0]-1, 0)
	cmdwin.keypad(1)
	cmdwin.nodelay(1)

	cmdstr = ""
	lines = []

def deinit():
	global cmdwin
	cmdwin.nodelay(0)
	cmdwin.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()

def addline(text):
	global outwin, lines

	x = str(text).strip()
	while len(x) > outwin.getmaxyx()[1]-1:
		y = x
		x = y[:outwin.getmaxyx()[1]-1]
		lines.append(x)
		x = y[len(x):]

	if len(x) > 0:
		lines.append(x)

	while len(lines) > outwin.getmaxyx()[0]:
		lines.pop(0)

	try:
		outwin.move(0, 0)
		for i in lines:
			outwin.clrtoeol()
			i = i.strip()
			outwin.addstr(i + "\n")
	except curses.error:
		pass
	outwin.noutrefresh()

def handle():
	global cmdwin, cmdstr

	cmdwin.timeout(0)
	c = cmdwin.getch()
	if c > -1:
		if c == 10:
			addline(cmdstr)
			cmdwin.clear()
			cmdstr = ""
		else:
			try:
				cmdwin.addch(c)
				cmdstr += chr(c)
			except curses.error:
				pass

	cmdwin.noutrefresh()
	curses.doupdate()

