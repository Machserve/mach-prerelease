# -*- coding: utf-8 -*-

import aiohttp
import time

from datetime import datetime

from aiohttp import web
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session


from mach_prerelease.utilities import send_email, send_text_message


class IndexView:
	"""View class for the index page."""
	async def get(request: aiohttp.web_request.Request):
		"""GET handler for the index page.

		Parameters
		----------
		request : aiohttp.web_request.Request
			The request sent by the client.
		"""
		session = await get_session(request)
		request.app["msg"] = None
		response = render_template("index.jinja2", request, {"session": session})
		response.headers["Content-Language"] = "en"
		return response


	async def post(request: aiohttp.web_request.Request):
		"""POST handler for the index page.
		
		Parameters
		----------
		request : aiohttp.web_request.Request
			The request sent by the client.

		FIXME: Expose session in Jinja2 template without context or request attribute?
		"""
		data = await request.post()
		session = await get_session(request)

		email = data.get("email")
		unix_now = time.time()
		datetime_now = datetime.now()
		text_message = "{email} joined the mailing list at {time}."
		flash_message = "Thank you for your interest. We will send an email to {email}."

		if "send_count" in session:
			# Check ratelimit
			if (unix_now - session["last_send"]) >= (60 * 3):
				session["send_count"] += 1
				session["last_send"] = unix_now
				request.app["msg"] = flash_message.format(email=email)
				send_text_message(text_message.format(email=email, time=datetime_now))
				send_email(email)
			else:
				request.app["msg"] = "Woah! You're requesting emails too quickly."
		
		if "send_count" not in session:
			session["send_count"] = 1
			session["last_send"] = unix_now
			request.app["msg"] = flash_message.format(email=email)
			send_text_message(text_message.format(email=email, time=datetime_now))
			send_email(email)
		
		# Get IP
		host, port = request.transport.get_extra_info("peername")
		entry = (email, datetime_now, host, port)
		print(entry)

		# Insert email, time, and IP into database
		
		response = render_template("index.jinja2", request, {"session": session})
		response.headers["Content-Language"] = "en"
		return response
