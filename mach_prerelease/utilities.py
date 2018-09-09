# -*- coding: utf-8 -*-

"""Utility functions and objects."""

import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client

from mach_prerelease.decorators import thread_task


@thread_task
def send_text_message(message: str) -> None:
	"""Send testing text messages.
	Currently, this is only used to notify me about 
	periodic tasks.
	
	Twilio's Client class automatically reads sid and token from
	the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables.
	
	Parameters
	----------
	message : str
		The message to be sent by SMS.
	"""
	Client().messages.create(
		to=os.environ["TWILIO_TARGET"], 
		from_=os.environ["TWILIO_NUMBER"],
		body=message,
	)


body = """
Hello,

Thank you for taking interest in our MLaaS platform.
We will notify you soon when we are ready for testers.

Many thanks,
The Machserve Development Team
"""

@thread_task
def send_email(email: str, body: str=body) -> None:
	"""Send an email to the prospective customer.

	Parameters
	----------
	email : str
		The email that was submitted.
	""" 

	from_address = os.environ.get("EMAIL_USER")
	try:
		msg = MIMEMultipart()
		msg["From"] = from_address
		msg["To"] = email
		msg["Subject"] = "Machserve Email Subscription"

		msg.attach(MIMEText(body, "plain"))

		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(from_address, os.environ.get("EMAIL_PASS"))
		server.sendmail(from_address, email, msg.as_string())
		server.quit()
	except:
		raise
