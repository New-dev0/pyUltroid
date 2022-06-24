import os
from urllib.parse import unquote
import time
from telethon.helpers import _maybe_await
from . import Var, fresh_install

try:
    import aiohttp
except ImportError:
    aiohttp = None
    import urllib

# ~~~~~~~~~~~~~~~~~~~~DDL Downloader~~~~~~~~~~~~~~~~~~~~
# @buddhhu @new-dev0


async def download_file(link, name):
    """for files, without progress callback with aiohttp"""
    if not aiohttp:
        urllib.request.urlretrieve(link, name)
        return name
    async with aiohttp.ClientSession() as ses:
        async with ses.get(link) as re_ses:
            with open(name, "wb") as f:
                f.write(await re_ses.read())
    return name


async def fast_download(download_url, filename=None, progress_callback=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                filename = unquote(download_url.rpartition("/")[-1])
            total_size = int(response.headers.get("content-length", 0)) or None
            downloaded_size = 0
            start_time = time.time()
            with open(filename, "wb") as f:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                    if progress_callback and total_size:
                        await _maybe_await(
                            progress_callback(downloaded_size, total_size)
                        )
            return filename, time.time() - start_time


GET_URL = f"https://raw.githubusercontent.com/{Var.GIT_EXT_PATH}/main/"
IgnoreFiles = []


async def get_file(path, name) -> str:
    path += ".py"
    name += ".py"
    if os.path.exists(name) and not fresh_install:
        return name
    if fresh_install:
        if name in IgnoreFiles:
            return name
        IgnoreFiles.append(name)
    return await download_file(GET_URL + path, name)
