
import os

from aiohttp import web

here = os.path.abspath(os.path.dirname(__file__))

class StaticFileHandler(object):
    """Async static file handler.
    
    FIXME: app['static_file_root'] for Jinja2
    
    See also
    --------
    https://github.com/aio-libs/aiohttp/issues/468
    """

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


    async def get_favicon(request):
        response = web.FileResponse(
            os.path.join(
                here, 
                "static", 
                "favicon.ico",
            )
        )
        return response
