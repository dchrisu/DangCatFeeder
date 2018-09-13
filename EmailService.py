import smtplib #smtplib library import
from datetime import datetime

#CD - Utilize the getEmailer during the call in order 
#		to send back a timestamp of when cats were fed!
#		Send email back to sender notifying them that cats
#		were successfully fed.
def sendMail(toAddress):
	smtpUser = '//////'
	smtpPass = '//////' #My password is not this, I changed it for protection! :)

	toAdd = toAddress
	fromAdd = smtpUser

        currentTime = datetime.now() 
        month = currentTime.month
        day = currentTime.day
        year = currentTime.year
        hour = currentTime.hour
        min = currentTime.minute
	timeOfDay = 'AM'
	strmin = str(min)

        if(hour == 12): 
		timeOfDay = 'PM'
	if(hour > 12):
		hour = hour-12
		timeOfDay = 'PM'
        if(min < 10): strmin = '0' + str(min)

        currentTime = str(month) + '/' + str(day) + '/' + str(year) + ', ' + str(hour) + ':' + strmin + ' ' + timeOfDay

	subject = 'Dang Cat Feeder - Row Row! Cats have been fed!'
	header = 'To: ' + toAdd + '\n' + 'from: ' + fromAdd + '\n' + 'Subject: ' + subject
	body = 'Hello, ' + '\n' + 'ROWWW ROWWWWWWWW! Cats have been fed at: ' + currentTime + '.' + '\n\n' + 'Lub,' + '\n' + 'Dang Cat Feeder' 

	print header + '\n' + body


	s = smtplib.SMTP('smtp.gmail.com', 587) 
	#makes instance variable, s, to connect to gmail server

	#encryption
	s.ehlo()
	s.starttls()
	s.ehlo()

	s.login(smtpUser, smtpPass) #login with credentials
	s.sendmail(fromAdd, toAdd, header + '\n\n' + body) 
	#declare to who it is sent, we need 2 new line breaks to separate

	s.quit() #close connection to server
	print 'Console: Fed e-mail has been sent successfully'

#CD - Mail sent to user who either did not input the
#		correct subject line input, or were not able to
#		feed cats
def sendFailMail(ToAddress, num):
	smtpUser = '//////' #Username email concealed for public!
	smtpPass = '//////' #Password is concealed for public!
	toAdd = ToAddress
	fromAdd = smtpUser
	subject = 'Dang Cat Feeder - Could not feed cats!'
	header = 'To: ' + toAdd + '\n' + 'from: ' + fromAdd + '\n' + 'Subject: ' + subject
	body = 'Hello, ' + '\n' + 'I couldn\'t feed the cats. :(' + '\n\n' + 'Lub, ' + '\n' + 'Dang Cat Feeder'
	subject2 = 'Dang Cat Feeder - Did not recognize your code input'
	extended = 'To: ' + toAdd + '\n' + 'from: ' + fromAdd + '\n' + 'Subject: ' + subject2
	body2 = 'Hello, ' + '\n' + 'I do not understand your code entry.' + '\n\n' + 'Lub, ' + '\n' + 'Dang Cat Feeder'

	#Special case when num == 1
	if(num == 1):
		print header + '\n' + body
	else:
		print extended + '\n' + body2

	s = smtplib.SMTP('smtp.gmail.com',587)
	s.ehlo()
	s.starttls()
	s.ehlo()

	s.login(smtpUser,smtpPass)

	if(num == 1):
		s.sendmail(fromAdd, toAdd, header + '\n\n' + body)
		print('Console: Successfully sent \"could not feed\" fail mail.')
	else:
		s.sendmail(fromAdd, toAdd, extended + '\n\n' + body2)
		print('Console: Successfully sent \"invalid subject code entry\" fail mail')

	s.quit()
