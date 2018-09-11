# -*- coding: utf-8 -*-

import asyncio
import time

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import aiohttp
from aiohttp import web
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session

from mach_prerelease.utilities import run_blocking_tasks, send_email, send_text_message
from mach_prerelease.controllers.firestore_client import FirestoreConnector


text_message = "{email} joined the mailing list at {time}."
flash_message = "Thank you for your interest. We will send an email to {email}."
already_on = "You are already on the mailing list."
firestore_connector = FirestoreConnector


async def check_email(email):
	results = await run_blocking_tasks(
				ThreadPoolExecutor(max_workers=3), 
				firestore_connector().validate_email, 
				email,
			)
	return results


async def onboard_prospective(request, email, datetime_now):
		request.app["msg"] = flash_message.format(email=email)
		request.app["error"] = None
		host, port = request.transport.get_extra_info("peername")
		data = {
			"email": email,
			"ip_address": host,
			"port": port,
			"date": datetime_now,
		}
		await run_blocking_tasks(
			ThreadPoolExecutor(max_workers=3), 
			firestore_connector().add_document, 
			data,
		)
		send_text_message(text_message.format(email=email, time=datetime_now))
		send_email(email)


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
		results = await check_email(email)

		if "send_count" in session:
			if (unix_now - session["last_send"]) >= (60 * 3):
				if False in results:
					request.app["msg"] = already_on
					request.app["error"] = True
				else:
					session["send_count"] += 1
					session["last_send"] = unix_now
					await onboard_prospective(request, email, datetime_now)
			else:
				request.app["msg"] = "Woah! Slow down! You're requesting emails too quickly."
				request.app["error"] = True
		elif "send_count" not in session:
			if False in results:
				request.app["msg"] = already_on
				request.app["error"] = True
			else:
				session["send_count"] = 1
				session["last_send"] = unix_now
				await onboard_prospective(request, email, datetime_now)

		response = render_template("index.jinja2", request, {"session": session})
		response.headers["Content-Language"] = "en"
		return response
