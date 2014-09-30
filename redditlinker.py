"""
redditlinker.py - A module to post links from irc to reddit
Copyright (C) 2014  Andy Chung - iamchung.com

iamchung.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from bs4 import BeautifulSoup
from willie.module import rate, rule
import willie
import praw
import urllib2

@willie.module.commands('redditlinker')
@rate(5)
def redditlinker(bot, trigger):
	bot.say(bot.config.redditlinker.message)

@rule(r'.*?((http[s]?|ftp)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
def redditlinkerlistener(bot, trigger):
	try:
		# extract link from text
		url = trigger.group(1)

		# go to link and see if there is title
		response = urllib2.urlopen(url)
		if response.headers.maintype != 'image':
			soup = BeautifulSoup(response.read(), from_encoding=response.info().getparam('charset'))
			title = soup.title
		else:
			title = url

		if title != '' and title != None:
			# start up reddit bot
			user_agent = ("Willie RedditLinker Module by gehsekky https://github.com/gehsekky/willie-redditlinker")
			reddit = praw.Reddit(user_agent=user_agent)
			reddit.login(bot.config.redditlinker.username, bot.config.redditlinker.password)
			subreddit = reddit.get_subreddit(bot.config.redditlinker.subreddit)
			subreddit.submit(title, url=url)
	except:
		pass # stealth mode. makes it hard to debug though so remove it.
