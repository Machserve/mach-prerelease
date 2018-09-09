
import os

from aiohttp import web

here = os.path.abspath(os.path.dirname(__file__))

class StaticFileHandler(object):
    """Async static file handler."""

    async def get_styles(request):
        response = web.FileResponse(
            os.path.join(
                here, 
                "static", 
                "styles.css",
            )
        )
        return response


    async def get_scripts(request):
        response = web.FileResponse(
            os.path.join(
                here, 
                "static", 
                "main.js",
            )
        )
        return response


    async def get_assets(request):
        response = web.FileResponse(
            os.path.join(
                here, 
                "static", 
                "particles.json",
            )
        )
        return response