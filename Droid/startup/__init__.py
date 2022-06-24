# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os, sys
import platform
from ..configs import Var
from ..functions.downloads import get_file
from telethon.sessions import StringSession

from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger


def where_hosted():
    if os.getenv("DYNO"):
        return "heroku"
    if os.getenv("RAILWAY_STATIC_URL"):
        return "railway"
    if os.getenv("OKTETO_TOKEN"):
        return "okteto"
    if os.getenv("KUBERNETES_PORT"):
        return "qovery | kubernetes"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "github actions"
    if os.getenv("ANDROID_ROOT"):
        return "termux"
    return "local"


from telethon import __version__
from telethon.tl.alltlobjects import LAYER

from ..version import __version__ as __pyUltroid__
from ..version import ultroid_version

file = "ultroid.log"

if os.path.exists(file):
    os.remove(file)

HOSTED_ON = where_hosted()
LOGS = getLogger("pyUltLogs")

_, v, __ = platform.python_version_tuple()

if int(v) < 10:
    from ._extra import _fix_logging

    _fix_logging(FileHandler)

if HOSTED_ON == "local":
    from ._extra import _ask_input

    _ask_input()

_LOG_FORMAT = "%(asctime)s | %(name)s [%(levelname)s] : %(message)s"
basicConfig(
    format=_LOG_FORMAT,
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler(file), StreamHandler()],
)
try:

    import coloredlogs

    coloredlogs.install(level=None, logger=LOGS, fmt=_LOG_FORMAT)
except ImportError:
    pass

LOGS.info(
    """
                    -----------------------------------
                            Starting Deployment
                    -----------------------------------
    """
)

LOGS.info(f"Python version - {platform.python_version()}")
LOGS.info(f"Telethon Version - {__version__} [Layer: {LAYER}]")
LOGS.info(f"X-Droid Version - {ultroid_version} [{HOSTED_ON}]")

try:
    from safety.tools import *
except ImportError:
    LOGS.error("'safety' package not found!")


def get_data(self_, key):
    data = self_.get(str(key))
    if data:
        try:
            data = eval(data)
        except BaseException:
            pass
    return data


async def UltroidDB():
    _ = "core/database/"
    TO = "Droid/startup/"
    if Var.REDIS_URI or Var.REDISHOST:
        from .. import HOSTED_ON

        try:
            from redis import Redis

            await get_file(f"{_}redisdb", f"{TO}redisdb")
            from Droid.startup.redisdb import Database

            return Database(
                host=Var.REDIS_URI or Var.REDISHOST,
                password=Var.REDIS_PASSWORD or Var.REDISPASSWORD,
                port=Var.REDISPORT,
                platform=HOSTED_ON,
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
            )
        except ImportError as e:
            LOGS.exception(e)
            LOGS.info("'redis' is not Installed.")
    if Var.MONGO_URI:
        try:
            from pymongo import MongoClient

            await get_file(f"{_}mongodb", f"{TO}mongodb")
            from Droid.startup.mongodb import Database

            return Database(Var.MONGO_URI)
        except ImportError:
            LOGS.error("'pymongo' not Installed.")
    if Var.DATABASE_URL:
        try:
            import psycopg2

            await get_file(f"{_}sqldb", f"{TO}sqldb")
            from Droid.startup.sqldb import Database

            return Database(Var.DATABASE_URL)
        except ImportError:
            LOGS.error("'psycopg2' is not Installed.")
    LOGS.critical(
        "No DB requirement fullfilled!\nPlease install redis, mongo or sql dependencies.."
    )
    exit()


def session_file(logger):
    if Var.SESSION:
        if len(Var.SESSION.strip()) != 353:
            logger.exception("Wrong string session. Copy paste correctly!")
            sys.exit()
        return StringSession(Var.SESSION)
    logger.exception("No String Session found. Quitting...")
    sys.exit()
