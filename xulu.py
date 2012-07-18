#!/usr/bin/env python
'''
Xulu IRC Bot Written by Arcalyth
'''

import traceback
from imp import reload

import irc
import xc
import cmdline

class xulu:
    nick = "Xulu"
    password = "tehXULU1"
    version = "v1.2"
    trigger = "?"

    def refresh():
        reload(xc)

def main():
	#cmdline.init()
	# [?] temporary until command parser/cli is up
	xc.connect(("<CONSOLE>", "<CONSOLE>", None, None), "irc.slashnet.org 6667")

	while True:
		for i in list(irc.socks.keys()):
			xulu_parse(i, irc.recv(i))

	#	cmdline.handle()

def xulu_parse(host, data):
	#cmdline.addline(data)
	if data == None:
		return None
	
	print(data)

	if len(data) == 0:
		return None
	elif data == "<IRC_CONNECTED>":
		irc.send(host, "MODE " + xulu.nick + " +B")
		irc.send(host, "PRIVMSG NickServ :IDENTIFY " + xulu.password)
		# [?] temporary until command parser/cli is up
		irc.send(host, "JOIN :#64digits")
	elif data[0] == "<IRC_NAMES>":
		pass
	elif data == "<IRC_ENDOFNAMES>":
		pass
	else:
		xFrom = data[0]
		xHost = data[1]
		xTo = data[2]
		xCmd = data[3]
		xPay = data[4][1:]

		# [?] CTCP VERSION
		if xCmd == "PRIVMSG" and xPay[0] == chr(1):
			if xPay[1:len(xPay)-1] == "VERSION":
				irc.send(host, "NOTICE " + xFrom + " :" + chr(1) + "VERSION Xulu IRC Bot " + xulu.version + " - Written by Arcalyth (arcalyth@socialgamer.net)" + chr(1))

		# [?] SocialGamer.net Bot Compliance (Respond to PRIVMSG help)
		if xCmd == "PRIVMSG" and xPay == "help" and xTo.lower() == xulu.nick.lower():
			irc.send(host, "PRIVMSG " + xFrom + " :Please use " + xulu.trigger + "help instead.")

		# [?] Connection Registration
		if xHost == "NOTICE" and xTo == "AUTH":
			# [?] RFC 2812 recommends NICK then USER
			irc.send(host, "NICK " + xulu.nick)
			irc.send(host, "USER " + xulu.nick + " 0 * :" + xulu.nick + " "	+ xulu.version + " by Arcalyth (arcalyth@socialgamer.net)")

		# [?] Respond to invites automatically
		if xCmd == "INVITE":
			irc.send(host, "JOIN " + xPay)

		# [?] Command Parser
		if xPay[0:len(xulu.trigger)] == xulu.trigger and xCmd == "PRIVMSG":
			reply = xTo
			if xTo == xulu.nick:
				reply = xFrom
			args = '("' + xFrom + '","' + xHost + '","' + reply + '","' + host + '")'
			index = xPay.find(" ")
			if index == -1:
				cmd = xPay[len(xulu.trigger):]
			else:
				cmd = xPay[len(xulu.trigger):index]
				args = args + ',"' + xPay[len(cmd)+2:] + '"'
			try:
				eval("xc." + cmd + "(" + args + ")")
			except AttributeError:
				irc.send(host, "PRIVMSG " + reply + " :No such command!")
#				cmdline.addline(traceback.format_exc())
			except TypeError:
				irc.send(host, "PRIVMSG " + reply + " :Invalid arguments.")
#				cmdline.addline(traceback.format_exc())
			except SyntaxError:
				pass
			except:
				print(traceback.format_exc())

#try:
#	main()
#except:
#	print((traceback.format_exc()))
#finally:
#	cmdline.deinit()
