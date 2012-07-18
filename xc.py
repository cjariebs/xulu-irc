import xulu

import irc
import re

xClass = xulu.xulu

def connect(sender, args):
	args = args.split(" ")
	host = args[0]
	port = 6667
	if len(args) > 1:
		port = int(args[1])
	irc.connect(host, port)

	# [?] RFC 2812 recommends NICK then USER
	irc.send(host, "NICK " + xClass.nick)
	irc.send(host, "USER " + xClass.nick + " 0 * :" + xClass.nick + " "	+ xClass.version + " by Arcalyth")
	

def reload(sender):
	try:
		xClass.refresh()
		irc.send(sender[3], "PRIVMSG " + sender[2] + " :Reloading commands.")
	except:
		raise

def say(sender, args="Say what?"):
	if re.match("^\W", args[0]) and args[0] != chr(1):
		return 0
	irc.send(sender[3], "PRIVMSG " + sender[2] + " :" + args)

def help(sender):
	irc.send(sender[3], "NOTICE " + sender[0] + " :No help file yet. Contact Arcalyth with questions.")

def idunno(sender):
	irc.send(sender[3], "PRIVMSG " + sender[2] + " :¯\(°_o)/¯")

def moo(sender, args=""):
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :          (__)")
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :          (oo)")
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :    /------\/ ")
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :   / |    ||  ")
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :  *  /\---/\  ")
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :     ~~   ~~  ")
	irc.send(sender[3], "PRIVMSG " + sender[0] + " :--- HAVE YOU MOOED TODAY? --- ")

def nick(sender, args="Xulu"):
	irc.send(sender[3], "NICK :" + args)

def part(sender):
	irc.send(sender[3], "PART " + sender[2] + " :Part requested by " + sender[0])

def convert(sender, args):
	irc.send(sender[3], "PRIVMSG " + sender[2] + " :Converting " + args[0] + " to its numeric value: " + str(ord(args[0])))

def rconvert(sender, args):
	irc.send(sender[3], "PRIVMSG " + sender[2] + " :Converting " + args + " from its numeric value: " + chr(int(args)))

def gtfo(sender):
	irc.send(sender[3], "QUIT " + xClass.nick + " " + xClass.version)

