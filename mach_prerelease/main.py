# -*- coding: utf-8 -*-


import asyncio
import base64
import logging
import os

import aiohttp_jinja2
import jinja2

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session import get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from mach_prerelease.views.views import IndexView

async def init_app() -> web.Application:
    """Initialize the async web application

    Returns
    -------
    web.Application
        An instance of the aiohttp web app using the default loop.
    """
    app = web.Application()

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader("mach_prerelease", "views/templates"),
    )
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_session(app, EncryptedCookieStorage(secret_key))
    app["static_root_url"] = os.environ.get("STATIC_PATH")
    app.router.add_get("/", IndexView.get)
    app.router.add_post("/", IndexView.post)

    return app


async def shutdown(app: web.Application):
    pass


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = init_app()
    web.run_app(app, shutdown_timeout=1.0)


if __name__ == "__main__":
    main()