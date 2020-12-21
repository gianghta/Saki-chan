import aiohttp
import asyncio


async def fetch(url):
    """ Execute an http call to url
    Args:
        session: context for making http call
        url: target URL
    Return:
        responses: A dict like object containing http response
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.json()
            return resp