#!/usr/bin/env python

from GmailWrapper import GmailWrapper
from EmailService import *
 
import RPi.GPIO as GPIO
import time
import smtplib
import imaplib

HOSTNAME = 'imap.gmail.com'		#Server Hostname		
USERNAME = '/////'				#Concealed personal information
PASSWORD = '/////'				#Concealed personal information

#Future ideas:
	#Fix SendConfirmationEmail
	#Confirm if get ToAddress works
	#Automate the emailing process?
	#Find out how to "get subject lines to customize rotations" (feed cats 3)
	#Add more functionalities?
		#LED physical confirmation
		#Log times and ETC about feedings
		#Customize motor more (maybe full 360 or customized size or portions)

	
#Inspiration code from: storiknow.com / Sam Storino
def feedByGmail():
    gmailWrapper = GmailWrapper(HOSTNAME, USERNAME, PASSWORD)
    ids = gmailWrapper.getIdsBySubject('feed cats')
    if(len(ids) > 0):
        try:
	    feed()
            emailer = getEmailer()
            sendMail(emailer)
	    gmailWrapper.markAsRead(ids)
	except:
	    emailer = getEmailer()
	    sendFailMail(emailer, 1)
	    gmailWrapper.markAsRead(ids)
	    print("Console: Failed to feed cats, they're starvinggggg")
    else:
	emailer = getEmailer()
	sendFailMail(emailer, 2)
	gmailWrapper.markAsRead(ids)

#CD - Custom Subject line inputs (feed cats a certain amount of times)
def trySubject(subject):
    gmailWrapper = GmailWrapper(HOSTNAME, USERNAME, PASSWORD)
    #number = the number that is in the subject string feed cats 
    number = subject[10:]
    subject = subject[:-2]
    print("Your current [subject] is " + subject + ".")
    print("Your current [number] is " + number  + ".")
    ids = gmailWrapper.getIdsBySubject(subject)
    if(len(ids) > 0):
        print("hit")
	try:
	    number = int(number)
	    if(number == 1):
		feedMe(1)
		print("I fed your cat one serving.")
	    if(number == 2):
		feedMe(2)
		print("I fed your cat two servings.")
	    if(number == 3):
		feedMe(3)
		print("I fed your cat three servings.")
	    gmailWrapper.markAsRead(ids)
	except:
	    print("Failed to feed cats specific number...")

#Utilize the server motor on GPIO port 18!
def feedMe(times):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    try:
	servo = GPIO.PWM(18, 50)
	servo.start(12.5)
	for index in range(0, times):
	    dutyCycle = 2.5 if (index % 2 == 0) else 12.5
	    servo.ChangeDutyCycle(dutyCycle)
	    time.sleep(0.8)
    finally:
        servo.stop()
	GPIO.cleanup()

#Credited from: storiknow.com / Sam Storino
def feed():
    # let the GPIO library know where we've connected our servo to the Pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
 
    try:
        servo = GPIO.PWM(18, 50)
        servo.start(12.5)
 
        # spin left, right, then left again rather than in a continuous circle
        # to prevent the food from jamming the servo
        for index in range(0, 3):
            dutyCycle = 2.5 if (index % 2 == 0) else 12.5
            servo.ChangeDutyCycle(dutyCycle)
            # adjust the sleep time to have the servo spin longer or shorter in that direction
            time.sleep(0.8) 
    finally:
        # always cleanup after ourselves
        servo.stop()
        GPIO.cleanup()

#CD - Fetch Emailer Address 
def getEmailer():
    mailServer = imaplib.IMAP4_SSL(HOSTNAME, 993)
    mailServer.login(USERNAME,PASSWORD)
    mailServer.list()
    mailServer.select('Inbox')
    typ, fetchedData1 = mailServer.search(None, 'ALL') 
    #fetch the first email; the 0'th email
    ids = fetchedData1[0]
    id_list = ids.split()
    
    #fetch most recent email id
    emailerID = int(id_list[-1])

    typ, fetchedData2 = mailServer.fetch(emailerID, '(BODY[HEADER.FIELDS (FROM)])')
    emailer = fetchedData2[0][1]
    emailer = cleanString(emailer)

    print 'Console: I retrieved the following from the gmail: ' + emailer + '.'
    mailServer.close()
    mailServer.logout()
    return emailer

#CD - Handle strings after fetching process. Parse out any non-desirable characters for prettiness
def cleanString(string):
    cleanedBefore = string.find('<') + 1
    cleanedAfter = string.find('>')
    cleaned = string[cleanedBefore:cleanedAfter]
    return cleaned

#CD - WIP GetSubject line method to fetch subject lines for custom inputs
def getSubject():
    
    gmailWrapper = GmailWrapper(HOSTNAME, USERNAME, PASSWORD)
    subject = '1'
    return subject

if __name__ == '__main__':
    # kick off the feeding process (move the servo)
    feedByGmail()
    #trySubject()
    #need to getSubject too.
