sopel-redditlinker
===================

a script to submit links posted in irc to a specified subreddit.

### requirements

This project requires the following:  

* [praw](https://praw.readthedocs.org/en/v2.1.16/) - Reddit API
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) - parsing library

you can install them via pip by doing something like:

    sudo pip install praw
    sudo pip install BeautifulSoup

### getting started

Place the following in the bottom of your sopel config file:

    [redditlinker]
    username = redditbotname
    password = redditbotpass
    subreddit = nameofsubredditpostingto
    message = a script to post links from irc to a subreddit
