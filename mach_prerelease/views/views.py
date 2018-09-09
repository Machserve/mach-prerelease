# -*- coding: utf-8 -*-

from datetime import datetime

import aiohttp

from aiohttp_jinja2 import render_template

from mach_prerelease.utilities import send_text_message

class IndexView:
	"""View class for the index page."""
	async def get(request: aiohttp.web_request.Request):
		"""GET handler for the index page.

		Parameters
		----------
		request : aiohttp.web_request.Request
			The request sent by the client.
		"""
		request.app["msg"] = None
		response = render_template("index.jinja2", request, {})
		response.headers["Content-Language"] = "en"
		return response


	async def post(request: aiohttp.web_request.Request):
		"""POST handler for the index page.
		
		Parameters
		----------
		request : aiohttp.web_request.Request
			The request sent by the client.
		"""
		data = await request.post()
		request.app["msg"] = f"Thank you for your interest. We will send an email to {data.get('email')}.",
		await send_text_message(f"{data.get('email')} joined the mailing list at {datetime.now()}" )
		response = render_template("index.jinja2", request, {})
		response.headers["Content-Language"] = "en"
		return response
