### Author: Enrique Herreros (eherrerosj@gmail.com)
### Django assignment for EverSnap. July 5th, 2014

import sys
from datetime import datetime, timedelta
import time
from celery.decorators import task
import logging
import smtplib
from datetime import timedelta
from celery.task.schedules import crontab 
from twython import Twython
from hashtag.models import Album, Picture
from django.db import IntegrityError
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)



@task()
def searchpics(hashtagi):
	results=""
	media_counter=0 # number of NEW pictures found every fetching
	APP_KEY = 'SK4xSopPESAeukCGMs0VMbfSt' # app key provided by Twitter
	APP_SECRET = '5xDyuqM2jHleEcEIx6VR2KwgrDuQydpE0L63koZT2qjf1cAhov' # private app password 
	twitter = Twython(APP_KEY, APP_SECRET) # create Twitter tunnel
	
	# Try to gather the last 'flag' (ie last id fetched), if there isn't, look for the last tweet to create a flag
	try:
		last_key = Picture.objects.order_by("-tweet_id").first() # last tweets id_str in our DB
	except Exception, e:
		search = twitter.search(q=hashtagi, count=1)
		last_key = search['statuses'][0]['id_str']
		pic = Picture(tweet_id=search['statuses'][0]['id_str'], url="http://INITIAL_flag", dateup=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datestored=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), owner=search['statuses'][0]['user']['screen_name'], likes=search['statuses'][0]['favorite_count'], album=Album.objects.get(hashtag=hashtagi))
		pic.save()
		return last_key # lets now wait for the next call

	# Fetch tweets since the last one we have in our DB
	search = twitter.search(q=hashtagi, since_id=last_key.tweet_id) # search for tweets with specified hashtag not fetched yet
	tweets = search['statuses'] # I dont need the metadata, only the statuses

	# Look for the album with the inputed hashtag, or we create a new album if it doesnt exist
	try:
		album = Album(hashtag=hashtagi)
		album.save()
		print "The new Album " + hashtagi + " has been created!"
	except IntegrityError:
		print "The Album " + hashtagi + " already exists"
		album = Album.objects.get(hashtag=hashtagi)

	# Gather data for each Tweet found under the hashtag, only store those that have media_url (pic.twitter...), the rest are going to raise
	#    an exception and will not be saved. Send email when the number of tweets in DB is multiple of 100. Optimized for minimum DB acceses
	try:
	    picamount = Picture.objects.count()
	    for idx, tweet in enumerate(tweets):
	        print 
	        try:
	            print "id_str:", tweet['id_str'], " URL:", tweet['entities']['media'][0]['media_url'], " Author:", tweet['user']['screen_name'], " Date:", tweet['created_at'], '\n', tweet['text'], "Favs:", tweet['favorite_count'], '\n\n'
	            pic = Picture(tweet_id=tweet['id_str'], url=tweet['entities']['media'][0]['media_url'], dateup=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), datestored=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), owner=tweet['user']['screen_name'], likes=tweet['favorite_count'], album=Album.objects.get(hashtag=hashtagi))
	            pic.save()
	            media_counter+=1
	            print "media_counter: " + str(media_counter)
	            print "media_counter+picamount: " + str(picamount+media_counter)
	            if ((picamount+media_counter)%100) == 0 and picamount < 501:
	                print "SENDING EMAIL"
	                send_email(from_addr=hashtagi + '@EversnapApp.com', to_addr_list=['kikexclusive@gmail.com'], cc_addr_list=['fonera.tfg@gmail.com'], bcc_addr_list='davide@geteversnap.com' ,subject=hashtagi + ' has ' + str(picamount+media_counter) + ' photos. ', msg='I\'m awesome!',login='fonera.tfg', password='foneratfg')
	        except Exception, e:
	            pass
	            # print "line", sys.exc_traceback.tb_lineno, ":", str(e)
	except:
	    pass

	print str(media_counter) + " NEW pictures were found in this round"

# Send email using python's smtplib module and gmail server.
def send_email(from_addr, to_addr_list, cc_addr_list, bcc_addr_list,
				subject, msg,
				login, password,
				smtpserver='smtp.gmail.com:587'):
	header = 'From: %s\n' % from_addr
	header += 'To: %s\n' % ','.join(to_addr_list)
	header += 'Cc: %s\n' % ','.join(cc_addr_list)
	header += 'Cc: %s\n' % ','.join(bcc_addr_list)
	header += 'Subject: %s\n\n' % subject
	msg = header + msg
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login, password)
	print server.sendmail(from_addr, to_addr_list, msg)
	server.quit()