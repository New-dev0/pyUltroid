# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import sys
from .version import __version__

import time, asyncio
from .configs import Var
from .startup import *
from .startup.BaseClient import UltroidClient

from .startup.funcs import _version_changes, update_envs
from .version import ultroid_version

start_time = time.time()
ult_cache = {}

loop = asyncio.get_event_loop()
run = loop.run_until_complete

udB = run(UltroidDB())
update_envs()

LOGS.info(f"Connecting to {udB.name}...")
if udB.ping():
    LOGS.info(f"Connected to {udB.name} Successfully!")

DUAL_MODE = udB.get_key("DUAL_MODE")

ultroid_bot = UltroidClient(
    session_file(LOGS),
    udB=udB,
    app_version=ultroid_version,
    device_model="X-Droid",
)

if not udB.get_key("BOT_TOKEN"):
    run(get_file("core/autobot", "Droid/startup/autobot"))
    from Droid.startup.autobot import autobot

    run(autobot())

asst = UltroidClient(None, bot_token=udB.get_key("BOT_TOKEN"), udB=udB)

if not asst.me.bot_inline_placeholder:
    ultroid_bot.run_in_loop(get_file("core/autobot", "Droid/startup/autobot"))
    from Droid.startup.autobot import enable_inline

    ultroid_bot.run_in_loop(enable_inline(ultroid_bot, asst.me.username))

_version_changes(udB)

HNDLR = udB.get_key("HNDLR") or "."
DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or HNDLR
