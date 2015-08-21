"""
redditlinker.py - A module to post links from irc to reddit
Copyright 2015, Andy Chung, iamchung.com
Licensed under the Eiffel Forum License 2.
"""

from bs4 import BeautifulSoup
from sopel.module import rate, rule
import sopel
import praw
import urllib2

@sopel.module.commands('redditlinker')
@rate(5)
def redditlinker(bot, trigger):
	# check to see if redditlinker section is in config
	if not hasattr(bot.config, 'redditlinker'):
		raise ValueError('No config section for redditlinker detected. Please make sure you set the options in the sopel config file.')

	# check for message setting. if none, provide default
	if not bot.config.redditlinker.message:
		bot.config.redditlinker.message = 'a script to post links from irc to a subreddit - https://github.com/gehsekky/sopel-redditlinker'
	bot.say(bot.config.redditlinker.message)

@rule(r'.*?((http[s]?|ftp)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
def redditlinkerlistener(bot, trigger):
	# check to see if redditlinker section is in config
	if not hasattr(bot.config, 'redditlinker'):
		raise ValueError('No config section for redditlinker detected. Please make sure you set the options in the sopel config file.')

	# checks for required settings
	if not bot.config.redditlinker.username:
		raise ValueError('No config setting for username found. Please enter the username of the reddit account to post from (karma should be high enough so it doesn\'t need to do captcha.')

	if not bot.config.redditlinker.password:
		raise ValueError('No config setting for password found. Please enter the password of the reddit account to post from.')

	if not bot.config.redditlinker.subreddit:
		raise ValueError('No config setting for subreddit found. Please enter the subreddit to post to.')

	# extract link from text
	url = trigger.group(1)

	try:
		# go to link and see if there is title
		response = urllib2.urlopen(url)
		if response.headers.maintype != 'image':
			soup = BeautifulSoup(response.read(), from_encoding=response.info().getparam('charset'))
			title = soup.title
		else:
			title = url

		if title != '' and title != None:
			# start up reddit bot
			user_agent = ("Sopel RedditLinker Module by gehsekky https://github.com/gehsekky/sopel-redditlinker")
			reddit = praw.Reddit(user_agent=user_agent)
			reddit.login(bot.config.redditlinker.username, bot.config.redditlinker.password)
			subreddit = reddit.get_subreddit(bot.config.redditlinker.subreddit)
			subreddit.submit(title, url=url)
	except:
		pass
