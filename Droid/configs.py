# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from decouple import config

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Var:
    # mandatory
    API_ID = config("API_ID", default=6, cast=int)
    API_HASH = config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    SESSION = config("SESSION", default=None)
    REDIS_URI = config("REDIS_URI", default=None) or config("REDIS_URL", default=None)
    REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
    GIT_EXT_PATH = config("GIT_EXT", default="New-dev0/Droid-Extension")

    # extras
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    LOG_CHANNEL = config("LOG_CHANNEL", default=0, cast=int)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    HEROKU_API = config("HEROKU_API", default=None)
    VC_SESSION = config("VC_SESSION", default=None)
    ADDONS = config("ADDONS", default=False, cast=bool)
    VCBOT = config("VCBOT", default=False, cast=bool)

    # for railway
    REDISPASSWORD = config("REDISPASSWORD", default=None)
    REDISHOST = config("REDISHOST", default=None)
    REDISPORT = config("REDISPORT", default=None)
    REDISUSER = config("REDISUSER", default=None)

    # for sql
    DATABASE_URL = config("DATABASE_URL", default=None)

    # for MONGODB users
    MONGO_URI = config("MONGO_URI", default=None)

    # for Okteto Platform
    OKTETO = config("OKTETO", cast=bool, default=False)

    INCLUDE_PLUGINS = config("INCLUDE_PLUGINS", default="")
