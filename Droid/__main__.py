# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from . import *

import os
import sys
import time

from .functions.helper import time_formatter, updater
from .startup.funcs import (
    WasItRestart,
    ready,
    startup_stuff,
)

# from .startup.loader import load_other_plugins

# Option to Auto Update On Restarts..
if (
    udB.get_key("UPDATE_ON_RESTART")
    and os.path.exists(".git")
    and ultroid_bot.run_in_loop(updater())
):
    os.system("git pull -f -q && pip3 install --no-cache-dir -U -q -r requirements.txt")

    os.execl(sys.executable, "python3", "-m", "pyUltroid")

ultroid_bot.run_in_loop(startup_stuff())

ultroid_bot.me.phone = None
ultroid_bot.first_name = ultroid_bot.me.first_name

if not ultroid_bot.me.bot:
    udB.set_key("OWNER_ID", ultroid_bot.uid)

LOGS.info("Initialising...")

LOGCH = udB.get_key("LOG_CHANNEL")
_run = True
if LOGCH:
    try:
        ultroid_bot.run_in_loop(ultroid_bot.get_entity(LOGCH))
        _run = False
    except Exception as er:
        LOGS.exception(er)
if _run:
    ultroid_bot.run_in_loop(get_file("core/autobot", "Droid/startup/autobot"))
    from .startup.autobot import autopilot

    ultroid_bot.run_in_loop(autopilot())

addons = udB.get_key("ADDONS") or Var.ADDONS

if HOSTED_ON == "termux" and udB.get_key("EXCLUDE_OFFICIAL") is None:
    _plugins = "autocorrect autopic compressor forcesubscribe gdrive glitch instagram nsfwfilter nightmode pdftools writer youtube"
    udB.set_key("EXCLUDE_OFFICIAL", _plugins)

load_plugins(addons=addons)

suc_msg = """
----------------------------------------------------------------------
Ultroid has been deployed! Visit @TheUltroid for updates!!
----------------------------------------------------------------------
"""

# Send/Ignore Deploy Message..
if not udB.get_key("LOG_OFF"):
    ultroid_bot.run_in_loop(ready())

# Edit Restarting Message (if It's restarting)
ultroid_bot.run_in_loop(WasItRestart(udB))

try:
    cleanup_cache()
except BaseException:
    pass

LOGS.info(f"Took {time_formatter((time.time() - start_time)*1000)} to start •ULTROID•")
LOGS.info(suc_msg)

asst.run()
